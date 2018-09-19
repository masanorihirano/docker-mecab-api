# coding: utf-8
from flask import Flask, abort, jsonify, request
import MeCab

mecab_wakati = MeCab.Tagger("-Owakati")
mecab = MeCab.Tagger()

api = Flask(__name__)
api.config['JSON_AS_ASCII'] = False

@api.route('/mecab/v1/wakati', methods=['POST'])
def wakati_post():
    if not request.json:
        abort(400)
    return wakati(request.json)

@api.route('/mecab/v1/wakati', methods=['GET'])
def wakati_get():
    if not request.args:
        abort(400)
    return wakati(request.args)

@api.route('/mecab/v1/original/wakati', methods=['POST'])
def wakati_original_post():
    if not request.json:
        abort(400)
    return wakati_original(request.json)

@api.route('/mecab/v1/original/wakati', methods=['GET'])
def wakati_original_get():
    if not request.args:
        abort(400)
    return wakati_original(request.args)

@api.route('/mecab/v1/analysis', methods=['POST'])
def analysis_post():
    if not request.json:
        abort(400)
    return analysis(request.json)

@api.route('/mecab/v1/analysis', methods=['GET'])
def analysis_get():
    if not request.args:
        abort(400)
    return analysis(request.args)

@api.route('/mecab/v1/original/analysis', methods=['POST'])
def analysis_original_post():
    if not request.json:
        abort(400)
    return analysis_original(request.json)

@api.route('/mecab/v1/original/analysis', methods=['GET'])
def analysis_original_get():
    if not request.args:
        abort(400)
    return analysis_original(request.args)

def wakati(target):
    try:
        if not ('sentence' in target):
            abort(400)
        sentence = target['sentence'].encode("utf-8")
        result = mecab_wakati.parse(sentence).split(" ")[:-1]
        return jsonify(wakati=result)
    except Exception as e:
        print(e)
        abort(500)

def wakati_original(target):
    try:
        if not ('sentence' in target):
            abort(400)
        sentence = target['sentence'].encode("utf-8")
        return mecab_wakati.parse(sentence)
    except Exception as e:
        print(e)
        abort(500)

def analysis(target):
    try:
        if not ('sentence' in target):
            abort(400)
        sentence = target['sentence'].encode("utf-8")
        analysis = mecab.parse(sentence)
        results = []
        for result in analysis.split("\n")[:-2]:
            [result1, stuff]= result.split("\t")
            [result2, result3, result4, result5, result6, result7, result8, result9, result10] = stuff.split(",")
            results.append({'表層形':result1, '品詞':result2, '品詞細分類1':result3, '品詞細分類2':result4,
                            '品詞細分類3':result5, '活用形':result6, '活用型':result7,'原型':result8,
                            '読み':result9,'発音':result10})
        return jsonify(analysis=results)
    except Exception as e:
        print(e)
        abort(500)

def analysis_original(target):
    try:
        if not ('sentence' in target):
            abort(400)
        sentence = target['sentence'].encode("utf-8")
        return mecab.parse(sentence)
    except Exception as e:
        print(e)
        abort(500)

# n-bestについては，なぜかpythonのラッパーで対応してないようなので，現時点ではコメントアウト．
"""
@api.route('/mecab/v1/analysis/<int:n_best>', methods=['POST'])
def analysis_n_best_post():
    if not request.json:
        abort(400)
    return analysis(n_best, request.json)

@api.route('/mecab/v1/analysis/<int:n_best>', methods=['POST'])
def analysis_n_best_get():
    if not request.args:
        abort(400)
    return analysis(n_best, request.args)

def analysis_n_best(n_best,target):
    try:
        if n_best <= 0:
            bad_url()
        if not ('sentence' in target):
            abort(400)
        sentence = target.json['sentence'].encode("utf-8")
        MeCab_n_best = MeCab.Tagger("-N"+str(n_best))
        analysis = MeCab_n_best.parse(sentence)
        results = []
        results_temp = []
        for result in analysis.split("\n"):
            print result
            if result == "EOS":
                results.append(results_temp)
                results_temp = []
                print "EOS"
                continue
            if result == "":
                continue
            [result1, stuff]= result.split("\t")
            [result2, result3, result4, result5, result6, result7, result8, result9, result10] = stuff.split(",")
            results_temp.append({'表層形':result1, '品詞':result2, '品詞細分類1':result3, '品詞細分類2':result4,
                            '品詞細分類3':result5, '活用形':result6, '活用型':result7,'原型':result8,
                            '読み':result9,'発音':result10})
        return jsonify(analysis=results)
    except Exception as e:
        print(e)
        abort(500)
"""

@api.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@api.errorhandler(405)
def not_allowed(error):
    return jsonify({'error': 'Method Not Allowed. You have to use POST method.'}), 405

@api.errorhandler(400)
def bad_post(error):
    return jsonify({'error': 'Input json needs sentence key.'}), 400

def bad_url():
    return jsonify({'error': 'n_best api needs positive integer for n_best.'}), 400

@api.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error.'}), 500

api.run(host='0.0.0.0', port=3001)

