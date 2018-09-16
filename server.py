# coding: utf-8
from flask import Flask, abort, jsonify, request
import MeCab

mecab_wakachi = MeCab.Tagger("-Owakati")
mecab = MeCab.Tagger()

api = Flask(__name__)
api.config['JSON_AS_ASCII'] = False

@api.route('/mecab/v1/wakachi', methods=['POST'])
def wakachi():
    try:
        if not (request.json and 'sentence' in request.json):
            abort(400)
        sentence = request.json['sentence']
        result = mecab_wakachi.parse(sentence.encode("utf-8")).split(" ")[:-1]
        return jsonify(wakachi=result,)
    except Exception as e:
        print(e)
        abort(500)

@api.route('/mecab/v1/analysis', methods=['POST'])
def analysis():
    try:
        if not (request.json and 'sentence' in request.json):
            abort(400)
        sentence = request.json['sentence'].encode("utf-8")
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

# n-bestについては，なぜかpythonのラッパーで対応してないようなので，現時点ではコメントアウト．
"""
@api.route('/mecab/v1/analysis/<int:n_best>', methods=['POST'])
def analysis_n_best(n_best):
    try:
        if n_best <= 0:
            bad_url()
        if not (request.json and 'sentence' in request.json):
            abort(400)
        sentence = request.json['sentence'].encode("utf-8")
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

