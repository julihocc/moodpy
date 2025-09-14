"""
Fourier Analysis

Subject Area: engineering

This module contains educational content generators for Fourier series,
Fourier transforms, and engineering applications in signal processing.
"""

import moodpy as me
import numpy.random as rnd
import math

label = "FOURIER_ANALYSIS"
miCabecera = """
<h1> Análisis de Fourier </h1>
<h2> Series de Fourier y Transformadas para Señales </h2>
"""

def gen(impr, cabecera=""):
    """Generate Fourier analysis problem."""
    
    # Choose problem type
    problem_types = ['fourier_series', 'fourier_coefficients', 'frequency_analysis', 'dft_properties']
    problem_type = rnd.choice(problem_types)
    
    if problem_type == 'fourier_series':
        # Generate a simple periodic function: f(x) = a₀ + a₁cos(x) + b₁sin(x)
        a0 = rnd.randint(-5, 5)
        a1 = rnd.randint(-4, 4)
        b1 = rnd.randint(-4, 4)
        
        # Ensure we have at least one non-zero coefficient
        if a0 == a1 == b1 == 0:
            a0 = rnd.choice([-2, -1, 1, 2])
        
        # Calculate RMS value and fundamental frequency amplitude
        rms_value = math.sqrt(a0**2 + (a1**2 + b1**2)/2)
        fundamental_amplitude = math.sqrt(a1**2 + b1**2)
        
        # Phase of fundamental component
        if a1 == 0 and b1 == 0:
            phase_rad = 0
            phase_deg = 0
        elif a1 == 0:
            phase_rad = math.pi/2 if b1 > 0 else -math.pi/2
        else:
            phase_rad = math.atan2(b1, a1)
        phase_deg = math.degrees(phase_rad)
        
        # Power in DC and fundamental
        dc_power = a0**2
        fundamental_power = (a1**2 + b1**2)/2
        total_power = dc_power + fundamental_power
        
        def format_term(coeff, term):
            if coeff == 0:
                return ""
            elif coeff == 1:
                return f" + {term}"
            elif coeff == -1:
                return f" - {term}"
            elif coeff > 0:
                return f" + {coeff}{term}"
            else:
                return f" - {abs(coeff)}{term}"
        
        # Build function string
        function_str = str(a0) if a0 != 0 else ""
        cos_term = format_term(a1, "\\cos(x)")
        sin_term = format_term(b1, "\\sin(x)")
        
        if not function_str and (cos_term or sin_term):
            # Handle case where a0 = 0
            function_str = cos_term.strip(" +") if cos_term else sin_term.strip(" +")
            if sin_term and cos_term:
                function_str = cos_term.strip(" +") + sin_term
        else:
            function_str += cos_term + sin_term
        
        if not function_str:
            function_str = "0"
        
        ejercicio = cabecera + f"""
        <p>
        Dada la función periódica representada por su serie de Fourier:
        </p>
        <p>
        $f(x) = {function_str}$
        </p>
        <p>
        Calcule las siguientes características de la señal:
        </p>
        <p>
        <strong>1. Valor RMS (eficaz):</strong> $f_{{rms}} = $ {me.NM(rms_value, error=0.001)}
        </p>
        <p>
        <strong>2. Amplitud de la componente fundamental:</strong> $A_1 = $ {me.NM(fundamental_amplitude, error=0.001)}
        </p>
        <p>
        <strong>3. Fase de la componente fundamental (radianes):</strong> $\\phi_1 = $ {me.NM(phase_rad, error=0.001)}
        </p>
        <p>
        <strong>4. Fase de la componente fundamental (grados):</strong> $\\phi_1 = $ {me.NM(phase_deg, error=0.1)}°
        </p>
        <p>
        <strong>5. Potencia de la componente DC:</strong> $P_{{DC}} = $ {me.NM(dc_power, error=0.001)}
        </p>
        <p>
        <strong>6. Potencia de la componente fundamental:</strong> $P_1 = $ {me.NM(fundamental_power, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Solución paso a paso:</strong>
        </p>
        <p>
        <strong>1. Identificación de coeficientes:</strong><br>
        Componente DC: $a_0 = {a0}$<br>
        Coeficiente coseno: $a_1 = {a1}$<br>
        Coeficiente seno: $b_1 = {b1}$
        </p>
        <p>
        <strong>2. Valor RMS (Teorema de Parseval):</strong><br>
        $f_{{rms}} = \\sqrt{{a_0^2 + \\frac{{1}}{{2}}\\sum_{{n=1}}^{{\\infty}}(a_n^2 + b_n^2)}}$<br>
        $= \\sqrt{{{a0}^2 + \\frac{{1}}{{2}}({a1}^2 + {b1}^2)}}$<br>
        $= \\sqrt{{{a0**2} + \\frac{{{a1**2 + b1**2}}}{{2}}}}$<br>
        $= \\sqrt{{{a0**2} + {(a1**2 + b1**2)/2}}} = {rms_value:.6f}$
        </p>
        <p>
        <strong>3. Amplitud de la fundamental:</strong><br>
        $A_1 = \\sqrt{{a_1^2 + b_1^2}} = \\sqrt{{{a1}^2 + {b1}^2}} = \\sqrt{{{a1**2 + b1**2}}} = {fundamental_amplitude:.6f}$
        </p>
        <p>
        <strong>4. Fase de la fundamental:</strong><br>
        $\\phi_1 = \\arctan\\left(\\frac{{b_1}}{{a_1}}\\right) = \\arctan\\left(\\frac{{{b1}}}{{{a1}}}\\right) = {phase_rad:.6f}$ rad = ${phase_deg:.2f}°$
        </p>
        <p>
        <strong>5. Análisis de potencia:</strong><br>
        Potencia DC: $P_{{DC}} = a_0^2 = {a0}^2 = {dc_power}$<br>
        Potencia fundamental: $P_1 = \\frac{{a_1^2 + b_1^2}}{{2}} = \\frac{{{a1**2} + {b1**2}}}{{2}} = {fundamental_power}$<br>
        Potencia total: $P_{{total}} = P_{{DC}} + P_1 = {dc_power} + {fundamental_power} = {total_power}$
        </p>
        <p>
        <strong>6. Representación alternativa:</strong><br>
        La componente fundamental puede escribirse como:<br>
        $A_1\\cos(x + \\phi_1) = {fundamental_amplitude:.3f}\\cos(x + {phase_rad:.3f})$
        </p>
        <p>
        <strong>Aplicaciones en ingeniería:</strong><br>
        El análisis de Fourier es fundamental en procesamiento de señales,
        análisis de vibraciones, sistemas de control, y diseño de filtros.
        </p>
        """
    
    elif problem_type == 'fourier_coefficients':
        # Calculate Fourier coefficients for simple periodic functions
        func_types = ['square_wave', 'sawtooth', 'triangle']
        func_type = rnd.choice(func_types)
        
        if func_type == 'square_wave':
            # Square wave coefficients: a₀ = 0, aₙ = 0, bₙ = 4/(nπ) for odd n, 0 for even n
            amplitude = rnd.randint(1, 5)
            
            # Calculate first few non-zero coefficients
            b1 = 4 * amplitude / math.pi
            b3 = 4 * amplitude / (3 * math.pi)
            b5 = 4 * amplitude / (5 * math.pi)
            
            ejercicio = cabecera + f"""
            <p>
            Calcule los coeficientes de Fourier para una onda cuadrada de amplitud {amplitude}
            con período $T = 2\\pi$:
            </p>
            <p>
            $f(x) = \\begin{{cases}}
            {amplitude} & \\text{{si }} 0 < x < \\pi \\\\
            -{amplitude} & \\text{{si }} \\pi < x < 2\\pi
            \\end{{cases}}$
            </p>
            <p>
            <strong>1. Coeficiente DC:</strong> $a_0 = $ {me.NM(0, error=0.001)}
            </p>
            <p>
            <strong>2. Primer coeficiente seno:</strong> $b_1 = $ {me.NM(b1, error=0.001)}
            </p>
            <p>
            <strong>3. Tercer coeficiente seno:</strong> $b_3 = $ {me.NM(b3, error=0.001)}
            </p>
            <p>
            <strong>4. Quinto coeficiente seno:</strong> $b_5 = $ {me.NM(b5, error=0.001)}
            </p>
            <p>
            <strong>5. Segundo coeficiente seno:</strong> $b_2 = $ {me.NM(0, error=0.001)}
            </p>
            """
            
            retroalimentacion = f"""
            <p>
            <strong>Solución paso a paso:</strong>
            </p>
            <p>
            <strong>1. Coeficiente DC:</strong><br>
            $a_0 = \\frac{{1}}{{2\\pi}}\\int_0^{{2\\pi}} f(x) dx$<br>
            $= \\frac{{1}}{{2\\pi}}\\left[\\int_0^\\pi {amplitude} dx + \\int_\\pi^{{2\\pi}} (-{amplitude}) dx\\right]$<br>
            $= \\frac{{1}}{{2\\pi}}[{amplitude}\\pi - {amplitude}\\pi] = 0$
            </p>
            <p>
            <strong>2. Coeficientes coseno:</strong><br>
            Por simetría, la onda cuadrada es una función impar, por lo que $a_n = 0$ para todo $n \\geq 1$.
            </p>
            <p>
            <strong>3. Coeficientes seno:</strong><br>
            $b_n = \\frac{{1}}{{\\pi}}\\int_0^{{2\\pi}} f(x)\\sin(nx) dx$<br>
            $= \\frac{{1}}{{\\pi}}\\left[\\int_0^\\pi {amplitude}\\sin(nx) dx + \\int_\\pi^{{2\\pi}} (-{amplitude})\\sin(nx) dx\\right]$<br>
            $= \\frac{{{amplitude}}}{{\\pi}}\\left[-\\frac{{\\cos(nx)}}{{n}}\\right]_0^\\pi - \\frac{{{amplitude}}}{{\\pi}}\\left[-\\frac{{\\cos(nx)}}{{n}}\\right]_\\pi^{{2\\pi}}$<br>
            $= \\frac{{{amplitude}}}{{n\\pi}}[-\\cos(n\\pi) + 1 - \\cos(2n\\pi) + \\cos(n\\pi)]$<br>
            $= \\frac{{{amplitude}}}{{n\\pi}}[2 - 2\\cos(n\\pi)] = \\frac{{2{amplitude}}}{{n\\pi}}[1 - \\cos(n\\pi)]$
            </p>
            <p>
            <strong>4. Evaluación específica:</strong><br>
            Para $n$ impar: $\\cos(n\\pi) = -1$, entonces $b_n = \\frac{{4{amplitude}}}{{n\\pi}}$<br>
            Para $n$ par: $\\cos(n\\pi) = 1$, entonces $b_n = 0$<br><br>
            $b_1 = \\frac{{4 \\cdot {amplitude}}}{{1 \\cdot \\pi}} = {b1:.6f}$<br>
            $b_2 = 0$ (n par)<br>
            $b_3 = \\frac{{4 \\cdot {amplitude}}}{{3 \\cdot \\pi}} = {b3:.6f}$<br>
            $b_5 = \\frac{{4 \\cdot {amplitude}}}{{5 \\cdot \\pi}} = {b5:.6f}$
            </p>
            <p>
            <strong>5. Serie de Fourier completa:</strong><br>
            $f(x) = \\frac{{4{amplitude}}}{{\\pi}}\\left[\\sin(x) + \\frac{{\\sin(3x)}}{{3}} + \\frac{{\\sin(5x)}}{{5}} + \\ldots\\right]$<br>
            $= \\frac{{4{amplitude}}}{{\\pi}}\\sum_{{n=1,3,5,\\ldots}} \\frac{{\\sin(nx)}}{{n}}$
            </p>
            <p>
            <strong>Aplicaciones:</strong><br>
            Las ondas cuadradas aparecen en señales digitales, modulación PWM,
            y como señales de referencia en sistemas de control.
            </p>
            """
            
        elif func_type == 'sawtooth':
            # Sawtooth wave: f(x) = ax for 0 < x < 2π
            slope = rnd.randint(1, 4)
            
            # Coefficients: a₀ = aπ, aₙ = 0, bₙ = -2a/n
            a0 = slope * math.pi
            b1 = -2 * slope
            b2 = -slope
            b3 = -2 * slope / 3
            
            ejercicio = cabecera + f"""
            <p>
            Calcule los coeficientes de Fourier para una onda diente de sierra:
            </p>
            <p>
            $f(x) = {slope}x$ para $0 < x < 2\\pi$ (período $T = 2\\pi$)
            </p>
            <p>
            <strong>1. Coeficiente DC:</strong> $a_0 = $ {me.NM(a0, error=0.001)}
            </p>
            <p>
            <strong>2. Primer coeficiente seno:</strong> $b_1 = $ {me.NM(b1, error=0.001)}
            </p>
            <p>
            <strong>3. Segundo coeficiente seno:</strong> $b_2 = $ {me.NM(b2, error=0.001)}
            </p>
            <p>
            <strong>4. Tercer coeficiente seno:</strong> $b_3 = $ {me.NM(b3, error=0.001)}
            </p>
            <p>
            <strong>5. Todos los coeficientes coseno:</strong> $a_n = $ {me.NM(0, error=0.001)} para $n \\geq 1$
            </p>
            """
            
            retroalimentacion = f"""
            <p>
            <strong>Solución paso a paso:</strong>
            </p>
            <p>
            <strong>1. Coeficiente DC:</strong><br>
            $a_0 = \\frac{{1}}{{2\\pi}}\\int_0^{{2\\pi}} {slope}x \\, dx$<br>
            $= \\frac{{{slope}}}{{2\\pi}} \\cdot \\frac{{x^2}}{{2}}\\Big|_0^{{2\\pi}}$<br>
            $= \\frac{{{slope}}}{{4\\pi}} \\cdot (2\\pi)^2 = \\frac{{{slope} \\cdot 4\\pi^2}}{{4\\pi}} = {slope}\\pi = {a0:.6f}$
            </p>
            <p>
            <strong>2. Coeficientes coseno:</strong><br>
            $a_n = \\frac{{1}}{{\\pi}}\\int_0^{{2\\pi}} {slope}x \\cos(nx) \\, dx$<br>
            Usando integración por partes con $u = x$, $dv = \\cos(nx)dx$:<br>
            $= \\frac{{{slope}}}{{\\pi}}\\left[\\frac{{x\\sin(nx)}}{{n}} - \\int \\frac{{\\sin(nx)}}{{n}} dx\\right]_0^{{2\\pi}}$<br>
            $= \\frac{{{slope}}}{{\\pi}}\\left[\\frac{{x\\sin(nx)}}{{n}} + \\frac{{\\cos(nx)}}{{n^2}}\\right]_0^{{2\\pi}}$<br>
            Como $\\sin(2n\\pi) = 0$ y $\\cos(2n\\pi) = \\cos(0) = 1$:<br>
            $a_n = \\frac{{{slope}}}{{\\pi}}\\left[0 + \\frac{{1}}{{n^2}} - 0 - \\frac{{1}}{{n^2}}\\right] = 0$
            </p>
            <p>
            <strong>3. Coeficientes seno:</strong><br>
            $b_n = \\frac{{1}}{{\\pi}}\\int_0^{{2\\pi}} {slope}x \\sin(nx) \\, dx$<br>
            Usando integración por partes con $u = x$, $dv = \\sin(nx)dx$:<br>
            $= \\frac{{{slope}}}{{\\pi}}\\left[-\\frac{{x\\cos(nx)}}{{n}} + \\int \\frac{{\\cos(nx)}}{{n}} dx\\right]_0^{{2\\pi}}$<br>
            $= \\frac{{{slope}}}{{\\pi}}\\left[-\\frac{{x\\cos(nx)}}{{n}} + \\frac{{\\sin(nx)}}{{n^2}}\\right]_0^{{2\\pi}}$<br>
            $= \\frac{{{slope}}}{{\\pi}}\\left[-\\frac{{2\\pi \\cos(2n\\pi)}}{{n}} + 0 - 0 - 0\\right]$<br>
            $= -\\frac{{2{slope}\\pi}}{{n\\pi}} = -\\frac{{2{slope}}}{{n}}$
            </p>
            <p>
            <strong>4. Valores específicos:</strong><br>
            $b_1 = -\\frac{{2 \\cdot {slope}}}{{1}} = {b1}$<br>
            $b_2 = -\\frac{{2 \\cdot {slope}}}{{2}} = {b2}$<br>
            $b_3 = -\\frac{{2 \\cdot {slope}}}{{3}} = {b3:.6f}$
            </p>
            <p>
            <strong>5. Serie de Fourier completa:</strong><br>
            $f(x) = {slope}\\pi - 2{slope}\\sum_{{n=1}}^{{\\infty}} \\frac{{\\sin(nx)}}{{n}}$<br>
            $= {a0:.3f} - 2{slope}\\left[\\sin(x) + \\frac{{\\sin(2x)}}{{2}} + \\frac{{\\sin(3x)}}{{3}} + \\ldots\\right]$
            </p>
            """
        
        else:  # triangle wave
            amplitude = rnd.randint(2, 6)
            
            # Triangle wave coefficients: a₀ = 0, aₙ = 8A/(n²π²) for odd n, 0 for even n, bₙ = 0
            a1 = 8 * amplitude / (math.pi**2)
            a3 = 8 * amplitude / (9 * math.pi**2)
            a5 = 8 * amplitude / (25 * math.pi**2)
            
            ejercicio = cabecera + f"""
            <p>
            Calcule los coeficientes de Fourier para una onda triangular de amplitud {amplitude}:
            </p>
            <p>
            $f(x) = \\begin{{cases}}
            \\frac{{{amplitude}x}}{{\\pi}} & \\text{{si }} 0 < x < \\pi \\\\
            {amplitude} - \\frac{{{amplitude}x}}{{\\pi}} & \\text{{si }} \\pi < x < 2\\pi
            \\end{{cases}}$
            </p>
            <p>
            <strong>1. Coeficiente DC:</strong> $a_0 = $ {me.NM(amplitude/2, error=0.001)}
            </p>
            <p>
            <strong>2. Primer coeficiente coseno:</strong> $a_1 = $ {me.NM(a1, error=0.001)}
            </p>
            <p>
            <strong>3. Tercer coeficiente coseno:</strong> $a_3 = $ {me.NM(a3, error=0.001)}
            </p>
            <p>
            <strong>4. Quinto coeficiente coseno:</strong> $a_5 = $ {me.NM(a5, error=0.001)}
            </p>
            <p>
            <strong>5. Todos los coeficientes seno:</strong> $b_n = $ {me.NM(0, error=0.001)} para todo $n$
            </p>
            """
            
            retroalimentacion = f"""
            <p>
            <strong>Análisis de la onda triangular:</strong>
            </p>
            <p>
            <strong>1. Coeficiente DC:</strong><br>
            El valor promedio de la onda triangular es $\\frac{{{amplitude}}}{{2}}$.
            </p>
            <p>
            <strong>2. Simetría:</strong><br>
            La onda triangular es una función par, por lo que $b_n = 0$ para todo $n$.
            </p>
            <p>
            <strong>3. Coeficientes coseno:</strong><br>
            Para una onda triangular simétrica:<br>
            $a_n = \\frac{{8{amplitude}}}{{n^2\\pi^2}}$ para $n$ impar<br>
            $a_n = 0$ para $n$ par
            </p>
            <p>
            <strong>4. Cálculos específicos:</strong><br>
            $a_1 = \\frac{{8 \\cdot {amplitude}}}{{1^2 \\cdot \\pi^2}} = \\frac{{{8*amplitude}}}{{\\pi^2}} = {a1:.6f}$<br>
            $a_3 = \\frac{{8 \\cdot {amplitude}}}{{3^2 \\cdot \\pi^2}} = \\frac{{{8*amplitude}}}{{9\\pi^2}} = {a3:.6f}$<br>
            $a_5 = \\frac{{8 \\cdot {amplitude}}}{{5^2 \\cdot \\pi^2}} = \\frac{{{8*amplitude}}}{{25\\pi^2}} = {a5:.6f}$
            </p>
            <p>
            <strong>5. Serie de Fourier completa:</strong><br>
            $f(x) = \\frac{{{amplitude}}}{{2}} + \\frac{{8{amplitude}}}{{\\pi^2}}\\sum_{{n=1,3,5,\\ldots}} \\frac{{\\cos(nx)}}{{n^2}}$<br>
            $= {amplitude/2} + \\frac{{{8*amplitude}}}{{\\pi^2}}\\left[\\cos(x) + \\frac{{\\cos(3x)}}{{9}} + \\frac{{\\cos(5x)}}{{25}} + \\ldots\\right]$
            </p>
            <p>
            <strong>Convergencia:</strong><br>
            La serie converge más rápidamente que la onda cuadrada debido al factor $1/n^2$.
            </p>
            """
    
    elif problem_type == 'frequency_analysis':
        # Generate a signal with multiple frequency components
        freqs = [rnd.randint(1, 5), rnd.randint(6, 10)]  # Two different frequencies
        amps = [rnd.randint(2, 6), rnd.randint(1, 4)]    # Two different amplitudes
        
        # Signal: f(t) = A₁cos(2πf₁t) + A₂cos(2πf₂t)
        f1, f2 = freqs
        A1, A2 = amps
        
        # Calculate power spectrum
        power_f1 = A1**2 / 2
        power_f2 = A2**2 / 2
        total_power = power_f1 + power_f2
        
        # Calculate fundamental period (LCM of periods)
        # For simplicity, we don't need to calculate the fundamental period for this problem
        
        ejercicio = cabecera + f"""
        <p>
        Analice la señal compuesta:
        </p>
        <p>
        $f(t) = {A1}\\cos(2\\pi \\cdot {f1} \\cdot t) + {A2}\\cos(2\\pi \\cdot {f2} \\cdot t)$
        </p>
        <p>
        Determine las siguientes características espectrales:
        </p>
        <p>
        <strong>1. Potencia de la componente de {f1} Hz:</strong> $P_{{ {f1} }} = $ {me.NM(power_f1, error=0.001)}
        </p>
        <p>
        <strong>2. Potencia de la componente de {f2} Hz:</strong> $P_{{ {f2} }} = $ {me.NM(power_f2, error=0.001)}
        </p>
        <p>
        <strong>3. Potencia total de la señal:</strong> $P_{{total}} = $ {me.NM(total_power, error=0.001)}
        </p>
        <p>
        <strong>4. Frecuencia más baja presente:</strong> {me.NM(min(f1, f2), error=0.001)} Hz
        </p>
        <p>
        <strong>5. Ancho de banda de la señal:</strong> {me.NM(max(f1, f2) - min(f1, f2), error=0.001)} Hz
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Análisis de frecuencias:</strong>
        </p>
        <p>
        <strong>1. Identificación de componentes:</strong><br>
        La señal contiene dos componentes sinusoidales:<br>
        • Componente 1: Amplitud = {A1}, Frecuencia = {f1} Hz<br>
        • Componente 2: Amplitud = {A2}, Frecuencia = {f2} Hz
        </p>
        <p>
        <strong>2. Cálculo de potencias:</strong><br>
        Para una señal $A\\cos(2\\pi ft)$, la potencia es $P = \\frac{{A^2}}{{2}}$<br><br>
        Potencia componente {f1} Hz: $P_{{ {f1} }} = \\frac{{{A1}^2}}{{2}} = \\frac{{{A1**2}}}{{2}} = {power_f1}$<br>
        Potencia componente {f2} Hz: $P_{{ {f2} }} = \\frac{{{A2}^2}}{{2}} = \\frac{{{A2**2}}}{{2}} = {power_f2}$<br>
        Potencia total: $P_{{total}} = P_{{ {f1} }} + P_{{ {f2} }} = {power_f1} + {power_f2} = {total_power}$
        </p>
        <p>
        <strong>3. Análisis espectral:</strong><br>
        • Frecuencia mínima: {min(f1, f2)} Hz<br>
        • Frecuencia máxima: {max(f1, f2)} Hz<br>
        • Ancho de banda: {max(f1, f2)} - {min(f1, f2)} = {max(f1, f2) - min(f1, f2)} Hz
        </p>
        <p>
        <strong>4. Espectro de amplitud:</strong><br>
        El espectro muestra picos en:<br>
        • {f1} Hz con amplitud {A1}<br>
        • {f2} Hz con amplitud {A2}
        </p>
        <p>
        <strong>5. Densidad espectral de potencia:</strong><br>
        • δ({f1} Hz): {power_f1}<br>
        • δ({f2} Hz): {power_f2}
        </p>
        <p>
        <strong>Aplicaciones:</strong><br>
        Este tipo de análisis es fundamental en procesamiento de señales,
        comunicaciones, análisis de vibraciones, y diseño de filtros.
        </p>
        """
    
    else:  # dft_properties
        # Discrete Fourier Transform properties
        N = rnd.choice([4, 8])  # DFT length
        
        # Generate a simple sequence
        if N == 4:
            sequence = [rnd.randint(0, 8) for _ in range(4)]
        else:
            sequence = [rnd.randint(0, 6) for _ in range(8)]
        
        # Calculate some DFT properties
        dc_component = sum(sequence)
        energy = sum(x**2 for x in sequence)
        
        # Nyquist frequency
        fs = rnd.choice([100, 200, 500])  # Sampling frequency
        nyquist_freq = fs / 2
        freq_resolution = fs / N
        
        ejercicio = cabecera + f"""
        <p>
        Considere la secuencia discreta de {N} puntos muestreada a {fs} Hz:
        </p>
        <p>
        $x[n] = [{', '.join(map(str, sequence))}]$
        </p>
        <p>
        Calcule las siguientes propiedades de la DFT:
        </p>
        <p>
        <strong>1. Componente DC (k=0):</strong> $X[0] = $ {me.NM(dc_component, error=0.001)}
        </p>
        <p>
        <strong>2. Energía de la señal:</strong> $E = $ {me.NM(energy, error=0.001)}
        </p>
        <p>
        <strong>3. Frecuencia de Nyquist:</strong> $f_{{Nyquist}} = $ {me.NM(nyquist_freq, error=0.001)} Hz
        </p>
        <p>
        <strong>4. Resolución en frecuencia:</strong> $\\Delta f = $ {me.NM(freq_resolution, error=0.001)} Hz
        </p>
        <p>
        <strong>5. Número de puntos DFT:</strong> $N = $ {me.NM(N, error=0.001)}
        </p>
        """
        
        retroalimentacion = f"""
        <p>
        <strong>Propiedades de la DFT:</strong>
        </p>
        <p>
        <strong>1. Componente DC:</strong><br>
        $X[0] = \\sum_{{n=0}}^{{N-1}} x[n] = {' + '.join(map(str, sequence))} = {dc_component}$<br>
        Esta es la suma de todas las muestras (componente de frecuencia cero).
        </p>
        <p>
        <strong>2. Energía de la señal:</strong><br>
        $E = \\sum_{{n=0}}^{{N-1}} |x[n]|^2 = {' + '.join(f'{x}^2' for x in sequence)} = {energy}$<br>
        Por el teorema de Parseval: $E = \\frac{{1}}{{N}}\\sum_{{k=0}}^{{N-1}} |X[k]|^2$
        </p>
        <p>
        <strong>3. Parámetros de muestreo:</strong><br>
        Frecuencia de muestreo: $f_s = {fs}$ Hz<br>
        Período de muestreo: $T_s = \\frac{{1}}{{f_s}} = \\frac{{1}}{{{fs}}} = {1/fs:.6f}$ s<br>
        Frecuencia de Nyquist: $f_{{Nyquist}} = \\frac{{f_s}}{{2}} = \\frac{{{fs}}}{{2}} = {nyquist_freq}$ Hz
        </p>
        <p>
        <strong>4. Resolución en frecuencia:</strong><br>
        $\\Delta f = \\frac{{f_s}}{{N}} = \\frac{{{fs}}}{{{N}}} = {freq_resolution}$ Hz<br>
        Esta es la separación entre bins de frecuencia adyacentes.
        </p>
        <p>
        <strong>5. Bins de frecuencia:</strong><br>
        Los bins de frecuencia están en: $f_k = k \\cdot \\Delta f$ para $k = 0, 1, \\ldots, N-1$<br>
        """
        
        freq_bins = [k * freq_resolution for k in range(N)]
        for k, freq in enumerate(freq_bins):
            retroalimentacion += f"$f_{{{k}}} = {freq}$ Hz<br>"
        
        retroalimentacion += f"""
        </p>
        <p>
        <strong>6. Simetría de la DFT:</strong><br>
        Para señales reales, $X[k] = X^*[N-k]$ (simetría conjugada)<br>
        Solo los primeros {N//2 + 1} puntos contienen información única.
        </p>
        <p>
        <strong>Aplicaciones:</strong><br>
        La DFT es la base del análisis espectral digital, filtrado FFT,
        y procesamiento de señales en tiempo real.
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