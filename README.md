# docker-mecab
[Mecab](http://taku910.github.io/mecab/)をAPIとして動かす
docker-composeだけで動かせるサービス．

# 起動・終了方法
起動
```
docker-compose up -d
```

終了
```
docker-compose down
```

# 設定
初期設定では，localhostの5000番にバインドされるように作ってありますので，
接続先は```http://localhost:5000/```となります．

変更の必要があれば，```docker-compose.yml```のポートのバインド先をを5000から変更してください．

# 使用方法
## わかち書きモード
```/mecab/v1/wakahi```に
```
{"sentence":"日本語の文章}
```
をpostすると，
```
{"wakachi":["日本語","の","文章"]}
```
のようにわかち書きされて配列で返ってきます．

テストコード:
```
curl -H 'Content-Type:application/json' localhost:5000/mecab/v1/wakachi -d '{"sentence":"すもももももももものうち"}' -XPOST
```
結果:
```
{"wakachi":["すもも","も","もも","も","もも","の","うち"]}
```
整形後:
```
{
	"wakachi": [
		"すもも",
		"も",
		"もも",
		"も",
		"もも",
		"の",
		"うち"
	]
}
```

## 解析モード
```/mecab/v1/analysis```に同様にpostすると，
```
{"analysis":[{形態素1の結果},{形態素2の結果},...}
```
と返ってきます．それぞれの結果は，
```
{"原型":"日本語","品詞":"名詞","品詞細分類1":"一般","品詞細分類2":"*","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"ニホンゴ","表層形":"日本語","読み":"ニホンゴ"}
```
のようになっています．出力は[Mecab](http://taku910.github.io/mecab/)と同様に
keyに表層形,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音を含むようになっていますが，
keyの並びは崩れます．

テストコード:
```
curl -H 'Content-Type:application/json' localhost:5000/mecab/v1/analysis -d '{"sentence":"すもももももももものうち"}' -XPOST
```
結果:
```
{"analysis":[{"原型":"すもも","品詞":"名詞","品詞細分類1":"一般","品詞細分類2":"*","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"スモモ","表層形":"すもも","読み":"スモモ"},{"原型":"も","品詞":"助詞","品詞細分類1":"係助詞","品詞細分類2":"*","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"モ","表層形":"も","読み":"モ"},{"原型":"もも","品詞":"名詞","品詞細分類1":"一般","品詞細分類2":"*","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"モモ","表層形":"もも","読み":"モモ"},{"原型":"も","品詞":"助詞","品詞細分類1":"係助詞","品詞細分類2":"*","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"モ","表層形":"も","読み":"モ"},{"原型":"もも","品詞":"名詞","品詞細分類1":"一般","品詞細分類2":"*","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"モモ","表層形":"もも","読み":"モモ"},{"原型":"の","品詞":"助詞","品詞細分類1":"連体化","品詞細分類2":"*","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"ノ","表層形":"の","読み":"ノ"},{"原型":"うち","品詞":"名詞","品詞細分類1":"非自立","品詞細分類2":"副詞可能","品詞細分類3":"*","活用型":"*","活用形":"*","発音":"ウチ","表層形":"うち","読み":"ウチ"}]}
```
整形後:
```
{
	"analysis": [
		{
			"原型": "すもも",
			"品詞": "名詞",
			"品詞細分類1": "一般",
			"品詞細分類2": "*",
			"品詞細分類3": "*",
			"活用型": "*",
			"活用形": "*",
			"発音": "スモモ",
			"表層形": "すもも",
			"読み": "スモモ"
		},
		{
			"原型": "も",
			"品詞": "助詞",
			"品詞細分類1": "係助詞",
			"品詞細分類2": "*",
			"品詞細分類3": "*",
			"活用型": "*",
			"活用形": "*",
			"発音": "モ",
			"表層形": "も",
			"読み": "モ"
		},
		{
			"原型": "もも",
			"品詞": "名詞",
			"品詞細分類1": "一般",
			"品詞細分類2": "*",
			"品詞細分類3": "*",
			"活用型": "*",
			"活用形": "*",
			"発音": "モモ",
			"表層形": "もも",
			"読み": "モモ"
		},
		{
			"原型": "も",
			"品詞": "助詞",
			"品詞細分類1": "係助詞",
			"品詞細分類2": "*",
			"品詞細分類3": "*",
			"活用型": "*",
			"活用形": "*",
			"発音": "モ",
			"表層形": "も",
			"読み": "モ"
		},
		{
			"原型": "もも",
			"品詞": "名詞",
			"品詞細分類1": "一般",
			"品詞細分類2": "*",
			"品詞細分類3": "*",
			"活用型": "*",
			"活用形": "*",
			"発音": "モモ",
			"表層形": "もも",
			"読み": "モモ"
		},
		{
			"原型": "の",
			"品詞": "助詞",
			"品詞細分類1": "連体化",
			"品詞細分類2": "*",
			"品詞細分類3": "*",
			"活用型": "*",
			"活用形": "*",
			"発音": "ノ",
			"表層形": "の",
			"読み": "ノ"
		},
		{
			"原型": "うち",
			"品詞": "名詞",
			"品詞細分類1": "非自立",
			"品詞細分類2": "副詞可能",
			"品詞細分類3": "*",
			"活用型": "*",
			"活用形": "*",
			"発音": "ウチ",
			"表層形": "うち",
			"読み": "ウチ"
		}
	]
}
```

# Copyright
Copyright &copy; 2017-2018 · All rights reserved. · [Masanori HIRANO](https://mhirano.jp/)