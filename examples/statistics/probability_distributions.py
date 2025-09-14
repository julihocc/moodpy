"""
Probability Distributions Analysis

Subject Area: statistics

This module contains educational content generators for probability distributions,
parameter estimation, and statistical modeling with normal, binomial, and Poisson distributions.
"""

import moodpy as me
import numpy.random as rnd
from scipy import stats
import math

label = "PROBABILITY_DISTRIBUTIONS"
miCabecera = """
<h1> Análisis de Distribuciones de Probabilidad </h1>
<h2> Modelado Estadístico y Estimación de Parámetros </h2>
"""

def binomial_coefficient(n, k):
    """Calculate binomial coefficient C(n,k)."""
    if k > n or k < 0:
        return 0
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def gen(impr, cabecera=""):
    """Generate probability distribution analysis problem."""
    
    # Choose distribution type
    distributions = ['normal', 'binomial', 'poisson']
    dist_type = rnd.choice(distributions)
    
    if dist_type == 'normal':
        # Normal distribution parameters
        mu = rnd.randint(50, 150)
        sigma = rnd.randint(5, 25)
        
        # Generate questions about specific probabilities
        x1 = mu + rnd.normal(0, sigma * 0.8)
        x2 = mu + rnd.normal(0, sigma * 1.2)
        if x2 < x1:
            x1, x2 = x2, x1
            
        # Calculate probabilities
        prob_less = stats.norm.cdf(x1, mu, sigma)
        prob_between = stats.norm.cdf(x2, mu, sigma) - stats.norm.cdf(x1, mu, sigma)
        prob_greater = 1 - stats.norm.cdf(x2, mu, sigma)
        
        # Z-scores
        z1 = (x1 - mu) / sigma
        z2 = (x2 - mu) / sigma
        
        ejercicio = cabecera + f"""
        <p>
        Una variable aleatoria X sigue una distribución normal con media μ = {mu} 
        y desviación estándar σ = {sigma}.
        </p>
        <p>
        <strong>Notación:</strong> X ~ N({mu}, {sigma}²)
        </p>
        <p>
        Calcule las siguientes probabilidades:
        </p>
        <p>
        <strong>1. P(X < {x1:.2f}):</strong> {me.NM(prob_less, error=0.001)}
        </p>
        <p>
        <strong>2. P({x1:.2f} < X < {x2:.2f}):</strong> {me.NM(prob_between, error=0.001)}
        </p>
        <p>
        <strong>3. P(X > {x2:.2f}):</strong> {me.NM(prob_greater, error=0.001)}
        </p>
        <p>
        <strong>4. Puntaje Z para X = {x1:.2f}:</strong> {me.NM(z1, error=0.01)}
        </p>
        <p>
        <strong>5. Puntaje Z para X = {x2:.2f}:</strong> {me.NM(z2, error=0.01)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución para distribución normal:</strong>
        </p>
        <p>
        <strong>Estandarización:</strong><br>
        Para cualquier valor x: Z = (x - μ)/σ = (x - {mu})/{sigma}
        </p>
        <p>
        <strong>1. P(X < {x1:.2f}):</strong><br>
        Z₁ = ({x1:.2f} - {mu})/{sigma} = {z1:.4f}<br>
        P(X < {x1:.2f}) = P(Z < {z1:.4f}) = Φ({z1:.4f}) = {prob_less:.4f}
        </p>
        <p>
        <strong>2. P({x1:.2f} < X < {x2:.2f}):</strong><br>
        Z₂ = ({x2:.2f} - {mu})/{sigma} = {z2:.4f}<br>
        P({x1:.2f} < X < {x2:.2f}) = Φ({z2:.4f}) - Φ({z1:.4f})<br>
        = {stats.norm.cdf(z2):.4f} - {stats.norm.cdf(z1):.4f} = {prob_between:.4f}
        </p>
        <p>
        <strong>3. P(X > {x2:.2f}):</strong><br>
        P(X > {x2:.2f}) = 1 - P(X < {x2:.2f}) = 1 - Φ({z2:.4f})<br>
        = 1 - {stats.norm.cdf(z2):.4f} = {prob_greater:.4f}
        </p>
        <p>
        <strong>Interpretación:</strong><br>
        • La distribución normal es simétrica alrededor de μ = {mu}<br>
        • Aproximadamente 68% de los datos está dentro de ±1σ de la media<br>
        • Los puntajes Z indican cuántas desviaciones estándar está un valor de la media
        </p>
        """
        
    elif dist_type == 'binomial':
        # Binomial distribution parameters
        n = rnd.randint(10, 50)
        p = round(rnd.uniform(0.1, 0.9), 2)
        
        # Generate questions
        k1 = rnd.randint(0, n//3)
        k2 = rnd.randint(n//2, min(n, n//2 + 10))
        
        # Calculate probabilities
        prob_exact = stats.binom.pmf(k1, n, p)
        prob_at_most = stats.binom.cdf(k2, n, p)
        prob_at_least = 1 - stats.binom.cdf(k2-1, n, p)
        
        # Expected value and variance
        expected = n * p
        variance = n * p * (1 - p)
        std_dev = math.sqrt(variance)
        
        ejercicio = cabecera + f"""
        <p>
        Una variable aleatoria X sigue una distribución binomial con n = {n} ensayos 
        y probabilidad de éxito p = {p}.
        </p>
        <p>
        <strong>Notación:</strong> X ~ Binomial({n}, {p})
        </p>
        <p>
        Calcule las siguientes probabilidades y parámetros:
        </p>
        <p>
        <strong>1. P(X = {k1}):</strong> {me.NM(prob_exact, error=0.0001)}
        </p>
        <p>
        <strong>2. P(X ≤ {k2}):</strong> {me.NM(prob_at_most, error=0.001)}
        </p>
        <p>
        <strong>3. P(X ≥ {k2}):</strong> {me.NM(prob_at_least, error=0.001)}
        </p>
        <p>
        <strong>4. E(X) - Valor esperado:</strong> {me.NM(expected, error=0.01)}
        </p>
        <p>
        <strong>5. Var(X) - Varianza:</strong> {me.NM(variance, error=0.01)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución para distribución binomial:</strong>
        </p>
        <p>
        <strong>Función de probabilidad:</strong><br>
        P(X = k) = C(n,k) × p^k × (1-p)^(n-k)
        </p>
        <p>
        <strong>1. P(X = {k1}):</strong><br>
        P(X = {k1}) = C({n},{k1}) × {p}^{k1} × {1-p}^{n-k1}<br>
        = {binomial_coefficient(n, k1)} × {p**k1:.6f} × {(1-p)**(n-k1):.6f}<br>
        = {prob_exact:.6f}
        </p>
        <p>
        <strong>2. P(X ≤ {k2}):</strong><br>
        P(X ≤ {k2}) = Σ P(X = k) para k = 0, 1, ..., {k2}<br>
        = {prob_at_most:.4f} (función de distribución acumulada)
        </p>
        <p>
        <strong>3. P(X ≥ {k2}):</strong><br>
        P(X ≥ {k2}) = 1 - P(X ≤ {k2-1}) = 1 - {stats.binom.cdf(k2-1, n, p):.4f}<br>
        = {prob_at_least:.4f}
        </p>
        <p>
        <strong>4. Parámetros de la distribución:</strong><br>
        • E(X) = np = {n} × {p} = {expected:.2f}<br>
        • Var(X) = np(1-p) = {n} × {p} × {1-p} = {variance:.2f}<br>
        • σ = √Var(X) = {std_dev:.2f}
        </p>
        <p>
        <strong>Interpretación:</strong><br>
        En promedio, esperamos {expected:.1f} éxitos en {n} ensayos independientes 
        con probabilidad {p} de éxito en cada ensayo.
        </p>
        """
        
    else:  # Poisson
        # Poisson distribution parameter
        lambda_param = round(rnd.uniform(2, 15), 1)
        
        # Generate questions
        k1 = rnd.randint(0, int(lambda_param) + 3)
        k2 = rnd.randint(int(lambda_param), int(lambda_param) + 8)
        
        # Calculate probabilities
        prob_exact = stats.poisson.pmf(k1, lambda_param)
        prob_at_most = stats.poisson.cdf(k2, lambda_param)
        prob_at_least = 1 - stats.poisson.cdf(k2-1, lambda_param)
        
        # Expected value and variance (both equal to lambda)
        expected = lambda_param
        variance = lambda_param
        
        ejercicio = cabecera + f"""
        <p>
        Una variable aleatoria X sigue una distribución de Poisson con parámetro λ = {lambda_param}.
        </p>
        <p>
        <strong>Notación:</strong> X ~ Poisson({lambda_param})
        </p>
        <p>
        Calcule las siguientes probabilidades y parámetros:
        </p>
        <p>
        <strong>1. P(X = {k1}):</strong> {me.NM(prob_exact, error=0.0001)}
        </p>
        <p>
        <strong>2. P(X ≤ {k2}):</strong> {me.NM(prob_at_most, error=0.001)}
        </p>
        <p>
        <strong>3. P(X ≥ {k2}):</strong> {me.NM(prob_at_least, error=0.001)}
        </p>
        <p>
        <strong>4. E(X) - Valor esperado:</strong> {me.NM(expected, error=0.01)}
        </p>
        <p>
        <strong>5. Var(X) - Varianza:</strong> {me.NM(variance, error=0.01)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución para distribución de Poisson:</strong>
        </p>
        <p>
        <strong>Función de probabilidad:</strong><br>
        P(X = k) = (λ^k × e^(-λ)) / k!
        </p>
        <p>
        <strong>1. P(X = {k1}):</strong><br>
        P(X = {k1}) = ({lambda_param}^{k1} × e^(-{lambda_param})) / {k1}!<br>
        = ({lambda_param**k1:.4f} × {math.exp(-lambda_param):.6f}) / {math.factorial(k1)}<br>
        = {prob_exact:.6f}
        </p>
        <p>
        <strong>2. P(X ≤ {k2}):</strong><br>
        P(X ≤ {k2}) = Σ P(X = k) para k = 0, 1, ..., {k2}<br>
        = {prob_at_most:.4f} (función de distribución acumulada)
        </p>
        <p>
        <strong>3. P(X ≥ {k2}):</strong><br>
        P(X ≥ {k2}) = 1 - P(X ≤ {k2-1}) = 1 - {stats.poisson.cdf(k2-1, lambda_param):.4f}<br>
        = {prob_at_least:.4f}
        </p>
        <p>
        <strong>4. Parámetros de la distribución:</strong><br>
        • E(X) = λ = {expected}<br>
        • Var(X) = λ = {variance}<br>
        • σ = √λ = {math.sqrt(variance):.2f}
        </p>
        <p>
        <strong>Interpretación:</strong><br>
        La distribución de Poisson modela el número de eventos que ocurren en un 
        intervalo fijo cuando los eventos son independientes y ocurren a una tasa 
        constante promedio de {lambda_param} eventos por intervalo.
        </p>
        <p>
        <strong>Aplicaciones típicas:</strong><br>
        • Número de llamadas telefónicas por hora<br>
        • Defectos en manufactura por unidad de tiempo<br>
        • Llegadas de clientes por minuto<br>
        • Errores tipográficos por página
        </p>
        """
    
    if impr:
        print(f"<h1>{label}</h1>")
        print(miCabecera)
        print(ejercicio + retroalimentacion)
        print(64*"-")
    
    return me.pretty(ejercicio, retroalimentacion)

if __name__ == "__main__":
    print(f"<h1>{label}</h1>")
    print(miCabecera)
    me.quick(gen, label, 0, impr=True, cabecera=miCabecera)
    
    me.quick(gen, label, 5, impr=True, cabecera=miCabecera)
    
    me.quick(gen, label, 25, impr=False, cabecera=miCabecera)