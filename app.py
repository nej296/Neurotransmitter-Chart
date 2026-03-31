"""
Neurotransmitter Wheel Chart — Interactive Flask + D3.js Application
A visual reference for 108+ neurotransmitters mapped across concentric data rings.
Author: Nicholas Johnson — Computational Neuroscience, George Mason University
"""

from flask import Flask, render_template, jsonify
from nt_database import NT_DATABASE, CATEGORY_COLORS, EFFECT_COLORS, CATEGORIES

app = Flask(__name__, static_folder='assets', static_url_path='/assets')


@app.route('/')
def index():
    return render_template(
        'index.html',
        nt_data=NT_DATABASE,
        category_colors=CATEGORY_COLORS,
        effect_colors=EFFECT_COLORS,
        categories=CATEGORIES
    )


@app.route('/api/neurotransmitters')
def api_neurotransmitters():
    return jsonify({
        'neurotransmitters': NT_DATABASE,
        'category_colors': CATEGORY_COLORS,
        'effect_colors': EFFECT_COLORS,
        'categories': CATEGORIES
    })


if __name__ == '__main__':
    print("\n  Neurotransmitter Wheel Chart")
    print("  Open http://localhost:5000 in your browser\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
