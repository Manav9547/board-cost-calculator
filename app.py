# app.py (Flask backend)
from flask import Flask, render_template, request

app = Flask(__name__)

def get_items_by_thickness(choice):
    match choice:
        case 4:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 32, "rate": 0.72}, "GLU": {"qty": 1.120, "rate": 30.50}}
        case 6:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 96, "rate": 0.72}, "GLU": {"qty": 2.240, "rate": 30.50}}
        case 9:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 160, "rate": 0.72}, "GLU": {"qty": 3.360, "rate": 30.50}}
        case 12:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 224, "rate": 0.72}, "GLU": {"qty": 4.480, "rate": 30.50}}
        case 18:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 352, "rate": 0.72}, "GLU": {"qty": 6.72, "rate": 30.50}}
        case 25:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 192.249, "rate": 0.72}, "GLU": {"qty": 4.485, "rate": 30.50}, "FRAME": {"qty": 0.4, "rate": 520.26}, "FATTI": {"qty": 1.4, "rate": 160.47}}
        case 30:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 128.169, "rate": 0.72}, "GLU": {"qty": 4.485, "rate": 30.50}, "FRAME": {"qty": 0.587, "rate": 520.26}, "FATTI": {"qty": 2.348, "rate": 160.47}}
        case 35:
            return {"FACE": {"qty": 5.936, "rate": 15.26}, "CORE": {"qty": 192.249, "rate": 0.72}, "GLU": {"qty": 4.485, "rate": 30.50}, "FRAME": {"qty": 0.587, "rate": 520.26}, "FATTI": {"qty": 2.348, "rate": 160.47}}
        case _:
            return None

def calculate_quantities(new_area, items):
    original_area = 32
    scale_factor = new_area / original_area
    results = []
    total_amount = 0

    for item, data in items.items():
        adjusted_qty = data["qty"] * scale_factor
        amount = adjusted_qty * data["rate"]
        total_amount += amount
        results.append({"item": item, "qty": round(adjusted_qty, 4), "rate": data["rate"], "amount": round(amount, 2)})

    exps = total_amount * 0.118
    total_amount1 = total_amount + exps
    profit = total_amount1 * 0.165
    total_with_profit = total_amount1 + profit
    rate_per_sq_mtr = total_with_profit / new_area

    summary = {
        "total": round(total_amount, 2),
        "exps": round(exps, 2),
        "total1": round(total_amount1, 2),
        "profit": round(profit, 2),
        "final_total": round(total_with_profit, 2),
        "rate_per_sqm": round(rate_per_sq_mtr, 2)
    }

    return results, summary

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            thickness = int(request.form['thickness'])
            area = float(request.form['area'])
            items = get_items_by_thickness(thickness)
            if not items or area <= 0:
                raise ValueError("Invalid input.")
            results, summary = calculate_quantities(area, items)
            return render_template('index.html', results=results, summary=summary, thickness=thickness, area=area)
        except ValueError as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
