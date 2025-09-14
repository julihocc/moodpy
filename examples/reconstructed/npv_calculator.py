#!/usr/bin/env python3
"""
Net Present Value (VPN) Calculator Generator

Reconstructed from: library/2020-1 Matemáticas Financieras/Parcial 3/305 VPN/

This generator creates problems about calculating Net Present Value (NPV) for 
investment projects with variable cash flows and different compounding periods.

Mathematical Pattern Analysis from XML:
- Initial investment (negative cash flow at t=0)
- Series of positive cash flows over different periods
- Variable interest rates and compounding frequencies
- NPV calculation with present value discounting

Pattern Recognition:
- Investment amounts: 900k-1020k pesos
- Cash flows: 20k-300k pesos (random distribution)
- Periods: bimestral, trimestral, cuatrimestral
- Interest rates: 10-20% annual
- NPV results can be positive or negative
"""

import numpy as np
import sys
import os
from tabulate import tabulate

# Add src directory to path to import MoodPy modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from moodpy.generator import Generator
from moodpy.cloze import Cloze


class NPVGenerator(Generator):
    """Generator for Net Present Value calculation problems."""
    
    def __init__(self):
        super().__init__()
        self.set_lambdas()
        
    def set_lambdas(self):
        """Define parameter generation functions based on XML pattern analysis."""
        self.lambdas = {
            # Initial investment (negative)
            "investment": lambda k: -np.random.randint(900, 1100) * 1000,  # -900k to -1100k
            
            # Annual interest rate (percentage)
            "annual_rate": lambda k: np.round(np.random.uniform(8.0, 22.0), 2),
            
            # Compounding frequency (periods per year)
            "frequency": lambda k: np.random.choice([2, 3, 4, 6, 12]),  # bimestral, trimestral, etc.
            
            # Number of periods
            "n_periods": lambda k: np.random.randint(6, 13),  # 6-12 periods
            
            # Cash flows - using more realistic distribution
            "cf_base": lambda k: np.random.randint(20, 120) * 1000,  # Base cash flow 20k-120k
            "cf_variation": lambda k: np.random.uniform(0.5, 2.0),  # Variation factor
        }
        
        # Requirements for valid financial problem
        self.requirements = [
            "d['investment'] < 0",  # Investment must be negative
            "d['annual_rate'] > 0",  # Positive interest rate
            "d['frequency'] > 0",   # Valid compounding frequency
            "d['n_periods'] >= 4",  # Minimum periods for meaningful analysis
            "d['cf_base'] > 0",     # Positive cash flows
        ]
        
    def generate_cash_flows(self):
        """Generate realistic cash flow series."""
        if self.parameters is None:
            return []
            
        d = self.parameters
        n = d['n_periods']
        base = d['cf_base']
        variation = d['cf_variation']
        
        # Generate cash flows with some randomness around the base
        cash_flows = []
        for i in range(n):
            # Add some period-based variation
            period_factor = 1.0 + 0.1 * np.sin(i * np.pi / n)  # Slight seasonal variation
            noise_factor = np.random.uniform(0.7, 1.3)
            
            cf = base * variation * period_factor * noise_factor
            cash_flows.append(int(cf / 1000) * 1000)  # Round to nearest 1000
            
        return cash_flows
        
    def get_period_name(self):
        """Get period name based on frequency."""
        if self.parameters is None:
            return "Período"
            
        freq = self.parameters['frequency']
        period_names = {
            2: "Semestre",
            3: "Cuatrimestre", 
            4: "Trimestre",
            6: "Bimestre",
            12: "Mes"
        }
        return period_names.get(freq, "Período")
        
    def calculate_npv(self, cash_flows):
        """Calculate Net Present Value."""
        if self.parameters is None:
            return 0.0
            
        d = self.parameters
        
        # Periodic interest rate
        r_period = (d['annual_rate'] / 100) / d['frequency']
        
        # NPV calculation
        npv = d['investment']  # Initial investment (negative)
        
        for t, cf in enumerate(cash_flows, 1):
            present_value = cf / ((1 + r_period) ** t)
            npv += present_value
            
        return npv
        
    def create_cash_flow_table(self, cash_flows):
        """Create HTML table of cash flows."""
        if self.parameters is None:
            return ""
            
        period_name = self.get_period_name()
        
        # Prepare table data
        table_data = []
        
        # Investment row
        table_data.append(["Inversión", f"${self.parameters['investment']:,}"])
        
        # Cash flow rows
        for i, cf in enumerate(cash_flows, 1):
            table_data.append([f"{period_name} {i}", f"${cf:,}"])
            
        # Convert to HTML table
        return tabulate(table_data, tablefmt="html")
        
    def set_exercise(self):
        """Generate the complete exercise text with financial problem."""
        if self.parameters is None:
            return
            
        d = self.parameters
        
        # Generate cash flows and calculate NPV
        cash_flows = self.generate_cash_flows()
        npv = self.calculate_npv(cash_flows)
        table_html = self.create_cash_flow_table(cash_flows)
        
        # Determine compounding description
        freq_descriptions = {
            2: "semestralmente",
            3: "cuatrimestralmente", 
            4: "trimestralmente",
            6: "bimestralmente",
            12: "mensualmente"
        }
        compounding_desc = freq_descriptions.get(d['frequency'], f"{d['frequency']} veces por año")
        
        exercise_text = f"""
        <h1>Matemáticas Financieras</h1>
        <h2>Valor Presente Neto (VPN)</h2>
        
        <p>
        Calcule el valor presente neto del siguiente flujo de caja:
        </p>
        
        {table_html}
        
        <p>
        con un costo de capital de <strong>{d['annual_rate']}%</strong> anual, 
        compuesto <strong>{compounding_desc}</strong>.
        </p>
        
        <p>
        <strong>Valor Presente Neto:</strong> ${{1:NM:={npv:.2f}:{abs(npv * 0.01):.2f}}}
        </p>
        
        <h3>Interpretación</h3>
        <p>
        {"<strong>Proyecto VIABLE:</strong> El VPN es positivo, lo que indica que el proyecto genera valor." if npv > 0 
         else "<strong>Proyecto NO VIABLE:</strong> El VPN es negativo, lo que indica que el proyecto destruye valor."}
        </p>
        
        <h3>Fórmula utilizada</h3>
        <p>
        $$VPN = I_0 + \\sum_{{t=1}}^{{n}} \\frac{{FC_t}}{{(1+r)^t}}$$
        </p>
        <p>
        donde:
        </p>
        <ul>
        <li>\\(I_0\\) = Inversión inicial = ${d['investment']:,}</li>
        <li>\\(FC_t\\) = Flujo de caja en el período \\(t\\)</li>
        <li>\\(r\\) = Tasa de descuento por período = {(d['annual_rate']/100/d['frequency']):.4f}</li>
        <li>\\(n\\) = Número de períodos = {len(cash_flows)}</li>
        </ul>
        """
        
        super().set_exercise(exercise_text)


def main():
    """Demonstration of the NPV generator."""
    print("=== MoodPy v3.0.0 - Net Present Value Generator ===\n")
    
    # Create generator
    gen = NPVGenerator()
    
    # Generate parameters
    print("Generating random parameters...")
    gen.reload_parameters()
    gen.test_parameters()
    
    if gen.parameters is None:
        print("ERROR: Could not generate valid parameters")
        return
        
    print("Parameters generated successfully!")
    d = gen.parameters
    print(f"- Investment: ${d['investment']:,}")
    print(f"- Annual rate: {d['annual_rate']}%")
    print(f"- Compounding: {d['frequency']} times per year")
    print(f"- Periods: {d['n_periods']}")
    
    # Generate cash flows and calculate NPV
    cash_flows = gen.generate_cash_flows()
    npv = gen.calculate_npv(cash_flows)
    print(f"- NPV: ${npv:,.2f}")
    
    # Generate exercise
    gen.set_exercise()
    print("\nGenerate exercise successful!")
    print("Preview (first 300 characters):")
    print(gen.exercise_text[:300] + "..." if len(gen.exercise_text) > 300 else gen.exercise_text)
    
    # Optional: Create XML export
    print("\n" + "="*60)
    print("Creating Moodle XML export...")
    
    cloze = Cloze()
    cloze.generator = gen
    cloze.set_info("MATEMÁTICAS FINANCIERAS", "FIN", "Valor Presente Neto")
    
    # Generate 3 sample questions
    cloze.testing(n=3)
    print("Sample questions generated successfully!")
    print("Check TESTING-*.txt file for output")


if __name__ == "__main__":
    main()