import math
from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NETPHYLAX Equations Calculator</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #eef2f7; margin: 0; padding: 30px; display: flex; justify-content: center; }
        .calc-card { background: #ffffff; width: 100%; max-width: 600px; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); }
        h1, h3 { text-align: center; color: #1a202c; margin-top: 0; }
        .tabs { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 25px; justify-content: center; }
        .tabs a { text-decoration: none; color: #4a5568; background: #edf2f7; padding: 10px 16px; border-radius: 8px; font-weight: 600; font-size: 13px; transition: all 0.2s; }
        .tabs a.active { background: #2b6cb0; color: #ffffff; }
        .form-row { margin-bottom: 15px; }
        label { display: block; margin-bottom: 6px; font-weight: 600; color: #4a5568; font-size: 14px; }
        input, select { width: 100%; padding: 12px; border: 1px solid #cbd5e0; border-radius: 8px; box-sizing: border-box; font-size: 15px; }
        .matrix-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-bottom: 12px; }
        .matrix-row input { text-align: center; padding: 8px; }
        button { width: 100%; background: #2b6cb0; color: white; border: none; padding: 14px; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 15px; }
        button:hover { background: #2c5282; }
        .output { margin-top: 25px; background: #ebf8ff; border-left: 5px solid #2b6cb0; padding: 15px; border-radius: 6px; }
        .output-lbl { font-weight: bold; color: #2c5282; margin: 0 0 5px 0; font-size: 14px; }
        .output-val { margin: 0; color: #1a202c; font-size: 16px; font-weight: 600; white-space: pre-line; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #718096; border-top: 1px solid #e2e8f0; padding-top: 15px; }
    </style>
</head>
<body>

<div class="calc-card">
    <h1>NETPHYLAX EQUATIONS CALCULATOR</h1>
    
    <!-- Navigation Tabs -->
    <div class="tabs">
        <a href="/?mode=QE" class="{% if mode == 'QE' %}active{% endif %}">Quadratic Eq (QE)</a>
        <a href="/?mode=SE" class="{% if mode == 'SE' %}active{% endif %}">Simultaneous Eq (SE)</a>
        <a href="/?mode=MX" class="{% if mode == 'MX' %}active{% endif %}">Matrix (MX)</a>
        <a href="/?mode=PS" class="{% if mode == 'PS' %}active{% endif %}">Plane Shapes (PS)</a>
        <a href="/?mode=SI" class="{% if mode == 'SI' %}active{% endif %}">Simple Interest (SI)</a>
        <a href="/?mode=CI" class="{% if mode == 'CI' %}active{% endif %}">Compound Interest (CI)</a>
    </div>

    <!-- Active Form View -->
    <form action="/?mode={{ mode }}" method="POST">
        <input type="hidden" name="calculator_type" value="{{ mode }}">

        <!-- 1. QUADRATIC MODE -->
        {% if mode == 'QE' %}
            <h3>Quadratic Equation Mode</h3>
            <div class="form-row"><label>Coefficient of x² (a):</label><input type="number" step="any" name="quad_a" required></div>
            <div class="form-row"><label>Coefficient of x (b):</label><input type="number" step="any" name="quad_b" required></div>
            <div class="form-row"><label>Constant value (c):</label><input type="number" step="any" name="quad_c" required></div>
        {% endif %}

        <!-- 2. SIMULTANEOUS MODE -->
        {% if mode == 'SE' %}
            <h3>Simultaneous Equation Mode</h3>
            <h4>Equation 1</h4>
            <div class="form-row"><label>Coefficient of x (a1):</label><input type="number" step="any" name="sim_a1" required></div>
            <div class="form-row"><label>Coefficient of y (b1):</label><input type="number" step="any" name="sim_b1" required></div>
            <div class="form-row"><label>Output value (c1):</label><input type="number" step="any" name="sim_c1" required></div>
            <h4>Equation 2</h4>
            <div class="form-row"><label>Coefficient of x (a2):</label><input type="number" step="any" name="sim_a2" required></div>
            <div class="form-row"><label>Coefficient of y (b2):</label><input type="number" step="any" name="sim_b2" required></div>
            <div class="form-row"><label>Output value (c2):</label><input type="number" step="any" name="sim_c2" required></div>
        {% endif %}

        <!-- 3. MATRIX MODE -->
        {% if mode == 'MX' %}
            <h3>Matrix (i, j, k Boxes)</h3>
            
            <h4>The i box grid values:</h4>
            <div class="matrix-row">
                <input type="number" step="any" name="i_a" placeholder="a" required>
                <input type="number" step="any" name="i_b" placeholder="b" required>
                <input type="number" step="any" name="i_c" placeholder="c" required>
                <input type="number" step="any" name="i_d" placeholder="d" required>
            </div>

            <h4>The j box grid values:</h4>
            <div class="matrix-row">
                <input type="number" step="any" name="j_a" placeholder="a" required>
                <input type="number" step="any" name="j_b" placeholder="b" required>
                <input type="number" step="any" name="j_c" placeholder="c" required>
                <input type="number" step="any" name="j_d" placeholder="d" required>
            </div>

            <h4>The k box grid values:</h4>
            <div class="matrix-row">
                <input type="number" step="any" name="k_a" placeholder="a" required>
                <input type="number" step="any" name="k_b" placeholder="b" required>
                <input type="number" step="any" name="k_c" placeholder="c" required>
                <input type="number" step="any" name="k_d" placeholder="d" required>
            </div>
        {% endif %}

        <!-- 4. PLANE SHAPES AREA MODE -->
        {% if mode == 'PS' %}
            <h3>Area of Plane Shapes</h3>
            <div class="form-row">
                <label>Choose targeted shape geometry:</label>
                <select name="sub_shape" onchange="this.form.action='/?mode=PS'; this.form.submit();">
                    <option value="t" {% if sub_shape == 't' %}selected{% endif %}>Triangle (t)</option>
                    <option value="c" {% if sub_shape == 'c' %}selected{% endif %}>Circle (c)</option>
                    <option value="s" {% if sub_shape == 's' %}selected{% endif %}>Square (s)</option>
                    <option value="r" {% if sub_shape == 'r' %}selected{% endif %}>Rectangle (r)</option>
                    <option value="tr" {% if sub_shape == 'tr' %}selected{% endif %}>Trapezium (tr)</option>
                    <option value="p" {% if sub_shape == 'p' %}selected{% endif %}>Parallelogram (p)</option>
                    <option value="rh" {% if sub_shape == 'rh' %}selected{% endif %}>Rhombus (rh)</option>
                </select>
            </div>

            {% if sub_shape == 't' %}
                <div class="form-row"><label>Base dimension:</label><input type="number" step="any" name="t_base" required></div>
                <div class="form-row"><label>Height dimension:</label><input type="number" step="any" name="t_height" required></div>
            {% elif sub_shape == 'c' %}
                <div class="form-row"><label>Radius value:</label><input type="number" step="any" name="c_radius" required></div>
            {% elif sub_shape == 's' %}
                <div class="form-row"><label>Length value:</label><input type="number" step="any" name="s_length" required></div>
            {% elif sub_shape == 'r' %}
                <div class="form-row"><label>Length dimension:</label><input type="number" step="any" name="r_length" required></div>
                <div class="form-row"><label>Breadth dimension:</label><input type="number" step="any" name="r_breadth" required></div>
            {% elif sub_shape == 'tr' %}
                <div class="form-row"><label>Dimension value a:</label><input type="number" step="any" name="tr_a" required></div>
                <div class="form-row"><label>Base dimension b:</label><input type="number" step="any" name="tr_b" required></div>
                <div class="form-row"><label>Height parameter h:</label><input type="number" step="any" name="tr_h" required></div>
            {% elif sub_shape == 'p' %}
                <div class="form-row"><label>Base dimension:</label><input type="number" step="any" name="p_base" required></div>
                <div class="form-row"><label>Height dimension:</label><input type="number" step="any" name="p_height" required></div>
            {% elif sub_shape == 'rh' %}
                <div class="form-row"><label>Diagonal dimension 1:</label><input type="number" step="any" name="rh_d1" required></div>
                <div class="form-row"><label>Diagonal dimension 2:</label><input type="number" step="any" name="rh_d2" required></div>
            {% endif %}
        {% endif %}

        <!-- 5. SIMPLE INTEREST MODE -->
        {% if mode == 'SI' %}
            <h3>Simple Interest Calculation</h3>
            <div class="form-row"><label>Principal (P):</label><input type="number" step="any" name="si_p" required></div>
            <div class="form-row"><label>Rate % (R):</label><input type="number" step="any" name="si_r" required></div>
            <div class="form-row"><label>Time Horizon in Years (T):</label><input type="number" step="any" name="si_t" required></div>
        {% endif %}

        <!-- 6. COMPOUND INTEREST MODE -->
        {% if mode == 'CI' %}
            <h3>Compound Interest Calculation</h3>
            <div class="form-row"><label>Principal (P):</label><input type="number" step="any" name="ci_p" required></div>
            <div class="form-row"><label>Rate % (R):</label><input type="number" step="any" name="ci_r" required></div>
            <div class="form-row"><label>Time Horizon in Years (T):</label><input type="number" step="any" name="ci_t" required></div>
        {% endif %}
        <button type="submit">Compute Values</button>
    </form>

    <!-- Response Window Area -->
    {% if result %}
        <div class="output">
            <p class="output-lbl">Calculation Terminal Output:</p>
            <p class="output-val">{{ result }}</p>
        </div>
    {% endif %}

    <!-- Custom Contact Info Block -->
    <div class="footer">
        <p>Support Contact Email: opeyemiizaiah@gmail.com | Mobile: +2348111279976</p>
</div>
</body>
</html>
"""
@app.route('/', methods=['GET', 'POST'])
def index():
    mode = request.args.get('mode', 'QE')
    sub_shape = request.args.get('sub_shape', 't')
    result = None

    if request.method == 'POST':
        try:
            if mode == 'QE':
                a = float(request.form.get('quad_a', 1))
                b = float(request.form.get('quad_b', 0))
                c = float(request.form.get('quad_c', 0))
                
                # YOUR EXACT QUADRATIC LOGIC
                b1 = b * -1
                b2 = b * b 
                a1 = a * 2 
                ac = a * 4 * c
                bac = b2 - ac
            
                if bac < 0:
                    positive_bac = abs(bac)
                    bac2 = math.sqrt(positive_bac)
                    real_part  = b1 / a1
                    imaginary_part = bac2 / a1
                    result = f"X1 = {real_part} + {imaginary_part}i\nX2 = {real_part} - {imaginary_part}i"
                else:
                    bac2 = math.sqrt(bac)
                    x1 = (b1 + bac2) / a1
                    x2 = (b1 - bac2) / a1
                    result = f"X1 = {x1}, X2 = {x2}"

            elif mode == 'SE':
                a1 = float(request.form.get('sim_a1', 0))
                b1 = float(request.form.get('sim_b1', 0))
                c1 = float(request.form.get('sim_c1', 0))
                a2 = float(request.form.get('sim_a2', 0))
                b2 = float(request.form.get('sim_b2', 0))
                c2 = float(request.form.get('sim_c2', 0))

                # YOUR EXACT SIMULTANEOUS LOGIC
                a3 = a2 * a1
                a4 = a2 * b1
                a5 = a2 * c1
                a6 = a1 * b2
                a7 = a1 * c2
                b5 = a4 - a6
                b6 = a5 - a7

                if abs(b5) < 0.000001:
                    result = "Zero Error. Check equations."
                else:
                    y = b6 / b5
                    y2 = a4 * y
                    y3 = a5 - y2
                    x = y3 / a3
                    result = f"x = {x}\ny = {y}"

            elif mode == 'MX':
                ia = float(request.form.get('i_a', 0))
                ib = float(request.form.get('i_b', 0))
                ic = float(request.form.get('i_c', 0))
                id = float(request.form.get('i_d', 0))
                ja = float(request.form.get('j_a', 0))
                jb = float(request.form.get('j_b', 0))
                jc = float(request.form.get('j_c', 0))
                jd = float(request.form.get('j_d', 0))
                ka = float(request.form.get('k_a', 0))
                kb = float(request.form.get('k_b', 0))
                kc = float(request.form.get('k_c', 0))
                kd = float(request.form.get('k_d', 0))

                # YOUR EXACT MATRIX LOGIC
                i_result = (ia * id) - (ic * ib)
                j_result = (ja * jd) - (jc * jb)
                k_result = (ka * kd) - (kc * kb)
                result = f"Vector Product Result: ({i_result})i - ({j_result})j + ({k_result})k"

            elif mode == 'PS':
                sub_shape = request.form.get('sub_shape', sub_shape)
                # YOUR EXACT PLANE SHAPE LOGIC
                if sub_shape == 't':
                    result = f"Area = {0.5 * float(request.form.get('t_base', 0)) * float(request.form.get('t_height', 0))}"
                elif sub_shape == 'c':
                    result = f"Area = {3.142 * (float(request.form.get('c_radius', 0)) ** 2)}"
                elif sub_shape == 's':
                    result = f"Area = {float(request.form.get('s_length', 0)) ** 2}"
                elif sub_shape == 'r':
                    result = f"Area = {float(request.form.get('r_length', 0)) * float(request.form.get('r_breadth', 0))}"
                elif sub_shape == 'tr':
                    result = f"Area = {0.5 * (float(request.form.get('tr_a', 0)) + float(request.form.get('tr_b', 0))) * float(request.form.get('tr_h', 0))}"
                elif sub_shape == 'p':
                    result = f"Area = {float(request.form.get('p_base', 0)) * float(request.form.get('p_height', 0))}"
                elif sub_shape == 'rh':
                    result = f"Area = {0.5 * float(request.form.get('rh_d1', 0)) * float(request.form.get('rh_d2', 0))}"

            elif mode == 'SI':
                principal = float(request.form.get('si_p', 0))
                rate = float(request.form.get('si_r', 0))
                time = float(request.form.get('si_t', 0))
                
                # YOUR EXACT SIMPLE INTEREST LOGIC
                numerator_cal = principal * rate * time
                simple_interest = numerator_cal / 100
                total_payout = principal + simple_interest
                result = f"Simple Interest = {simple_interest:,.2f}\nTotal Payout = {total_payout:,.2f}"

            elif mode == 'CI':
                principal = float(request.form.get('ci_p', 0))
                rate = float(request.form.get('ci_r', 0))
                time = float(request.form.get('ci_t', 0))

                # YOUR EXACT COMPOUND INTEREST LOGIC
                r1 = rate / 100
                r2 = 1 + r1
                rt = r2 ** time
                a = principal * rt
                result = f"Compound Interest : {a:,.2f}"

        except ValueError:
            result = "Syntax Error! Enter a digit."

    from flask import render_template_string
    return render_template_string(HTML_TEMPLATE, mode=mode, sub_shape=sub_shape, result=result)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
