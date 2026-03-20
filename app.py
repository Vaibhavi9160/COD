from flask import Flask, render_template, request
import struct
import math

app = Flask(__name__)

# ---------- EXISTING FUNCTION (kept for accuracy) ----------
def float_to_bits_native(x, precision='single'):
    if precision == 'single':
        packed = struct.pack('!f', float(x))
        bits = ''.join(f'{b:08b}' for b in packed)
        hx = packed.hex()
    else:
        packed = struct.pack('!d', float(x))
        bits = ''.join(f'{b:08b}' for b in packed)
        hx = packed.hex()
    return bits, hx


# ---------- NEW STEP-BY-STEP FUNCTION ----------
def ieee_steps(num):
    steps = []

    if math.isnan(num):
        return ["Number is NaN → special IEEE representation"]
    if math.isinf(num):
        return ["Number is Infinity → exponent all 1s, mantissa 0"]

    # Step 1: Sign
    sign = 0 if num >= 0 else 1
    steps.append(f"Step 1: Sign bit = {sign}")

    num = abs(num)

    # Step 2: Convert to binary
    integer_part = int(num)
    fractional_part = num - integer_part

    int_bin = bin(integer_part)[2:] if integer_part != 0 else "0"

    frac_bin = ""
    frac = fractional_part
    for _ in range(10):  # limit length
        frac *= 2
        bit = int(frac)
        frac_bin += str(bit)
        frac -= bit

    steps.append(f"Step 2: Binary = {int_bin}.{frac_bin}")

    # Step 3: Normalize
    if integer_part != 0:
        shift = len(int_bin) - 1
        normalized = f"1.{int_bin[1:]}{frac_bin}"
    else:
        shift = -(frac_bin.find('1') + 1)
        normalized = f"1.{frac_bin[frac_bin.find('1')+1:]}"
    
    steps.append(f"Step 3: Normalized form = {normalized} × 2^{shift}")

    # Step 4: Exponent
    bias = 127
    exponent = shift + bias
    exp_bin = format(exponent, '08b')
    steps.append(f"Step 4: Exponent = {shift} + {bias} = {exponent} → {exp_bin}")

    # Step 5: Mantissa
    mantissa = normalized.split('.')[1][:23].ljust(23, '0')
    steps.append(f"Step 5: Mantissa = {mantissa}")

    return steps


# ---------- ROUTES ----------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    steps = None

    if request.method == "POST":
        user_input = request.form["number"]

        try:
            num = float(user_input)

            bits, hx = float_to_bits_native(num, 'single')
            steps = ieee_steps(num)

            result = {
                "number": num,
                "bits": bits,
                "hex": hx,
                "sign": bits[0],
                "exponent": bits[1:9],
                "mantissa": bits[9:]
            }

        except:
            result = {"error": "Invalid input"}

    return render_template("index.html", result=result, steps=steps)


if __name__ == "__main__":
    app.run(debug=True)