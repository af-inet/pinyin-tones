#!/usr/bin/env python3
import re
import sys

"""
Creates a MacOS text substitutions plist file that includes every pinyin + tone combination.
Example: replace ni3 with nǐ
"""

"""
1	When a syllable contains a single vowel only, the tone mark is placed above the vowel sound.	nǐ, mǎ, kè
2	When a syllable contains two or more vowels, the tone mark is usually placed above vowels in the order of a, o, e, i, u, ü	hǎo, xiè, guān
3	When a tone mark is placed above the vowel “i”, the dot over it should be omitted.	nín, jìn, shī
4	When “iu” or “ui” comes, the tone mark should be placed above the terminal vowel.	liú, guǐ
from: http://www.ichineselearning.com/learn/pinyin-tones.html
"""
# thanks to: https://stackoverflow.com/a/8200388
PinyinToneMark = {0: "aoeiuvü", 1: "āōēīūǖǖ", 2: "áóéíúǘǘ", 3: "ǎǒěǐǔǚǚ", 4: "àòèìùǜǜ"}


def decode_pinyin(s):
    s = s.lower()
    r = ""
    t = ""
    for c in s:
        if c >= "a" and c <= "z":
            t += c
        elif c == ":":
            assert t[-1] == "u"
            t = t[:-1] + "\u00fc"
        else:
            if c >= "0" and c <= "5":
                tone = int(c) % 5
                if tone != 0:
                    m = re.search("[aoeiuv\u00fc]+", t)
                    if m is None:
                        t += c
                    elif len(m.group(0)) == 1:
                        t = (
                            t[: m.start(0)]
                            + PinyinToneMark[tone][PinyinToneMark[0].index(m.group(0))]
                            + t[m.end(0) :]
                        )
                    else:
                        if "a" in t:
                            t = t.replace("a", PinyinToneMark[tone][0])
                        elif "o" in t:
                            t = t.replace("o", PinyinToneMark[tone][1])
                        elif "e" in t:
                            t = t.replace("e", PinyinToneMark[tone][2])
                        elif t.endswith("ui"):
                            t = t.replace("i", PinyinToneMark[tone][3])
                        elif t.endswith("iu"):
                            t = t.replace("u", PinyinToneMark[tone][4])
                        else:
                            t += "!"
            r += t
            t = ""
    r += t
    return r


# thanks to: http://www.quickmandarin.com/chinesepinyintable/
all_pinyin = """
bo	ba	bo		bai	bei	bao		ban	ben	bang	beng		bu									bi		bie	biao		bian		bin	bing					
po	pa	po		pai	pei	pao	pou	pan	pen	pang	peng		pu									pi		pie	piao		pian		pin	ping					
mo	ma	mo	me	mai	mei	mao	mou	man	men	mang	meng		mu									mi		mie	miao	miu	mian		min	ming					
fo	fa	fo			fei		fou	fan	fen	fang	feng		fu																						
de	da		de	dai	dei	dao	dou	dan	den	dang	deng	dong	du		duo		dui	duan		dun		di	dia	die	diao	diu	dian			ding					
te	ta		te	tai	tei	tao	tou	tan		tang	teng	tong	tu		tuo		tui	tuan		tun		ti		tie	tiao		tian								
ne	na		ne	nai	nei	nao	nou	nan	nen	nang	neng	nong	nu		nuo			nuan		nun		ni		nie	niao	niu	nian	niang	nin	ning		nü	nüe		
le	la		le	lai	lei	lao	lou	lan		lang	leng	long	lu		luo			luan		lun		li	lia	lie	liao	liu	lian	liang	lin	ling		lü	lüe		
ge	ga		ge	gai	gei	gao	gou	gan	gen	gang	geng	gong	gu	gua	guo	guai	gui	guan	guang	gun															
ke	ka		ke	kai	kei	kao	kou	kan	ken	kang	keng	kong	ku	kua	kuo	kuai	kui	kuan	kuang	kun															
he	ha		he	hai	hei	hao	hou	han	hen	hang	heng	hong	hu	hua	huo	huai	hui	huan	huang	hun															
zi	za		ze	zai	zei	zao	zou	zan	zen	zang	zeng	zong	zu		zuo		zui	zuan		zun		zi													
ci	ca		ce	cai		cao	cou	can	cen	cang	ceng	cong	cu		cuo		cui	cuan		cun		cin													
si	sa		se	sai		sao	sou	san	sen	sang	seng	song	su		suo		sui	suan		sun		si													
zhi	zha		zhe	zhai	zhei	zhao	zhou	zhan	zhen	zhang	zheng	zhong	zhu	zhua	zhuo	zhuai	zhui	zhuan	zhuang	zhun		zhi													
chi	cha		che	chai		chao	chou	chan	chen	chang	cheng	chong	chu	chua	chuo	chuai	chui	chuan	chuang	chun		chi													
shi	sha		she	shai	shei	shao	shou	shan	shen	shang	sheng		shu	shua	shuo	shuai	shui	shuan	shuang	shun		shi													
ri			re			rao	rou	ran	ren	rang	reng	rong	ru	rua	ruo		rui	ruan		run		ri													
ji																						ji	jia	jie	jiao	jiu	jian	jiang	jin	jing	jiong	ju	jue	juan	jun
qi																						qi	qia	qie	qiao	qiu	qian	qiang	qin	qing	qiong	qu	que	quan	qun
xi																						xi	xia	xie	xiao	xiu	xian	xiang	xin	xing	xiong	xu	xue	xuan	xun
    a	o	e	ai	ei	ai	ao	ou	an	en	ang	ong	wu	wa	wo	wai	wei	wan	wang	wen	weng	yi	ya	ye	yao	you	yan	yang	yin	ying	yong	yu	yue	yuan	yun
"""

all_pinyin = all_pinyin.replace("ü", "v")

plist_template_start = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
"""

plist_template_end = """</array>
</plist>
"""

plist_entry = """	<dict>
		<key>phrase</key>
		<string>{output}</string>
		<key>shortcut</key>
		<string>{input}</string>
	</dict>
"""

if __name__ == "__main__":
    sys.stdout.write(plist_template_start)
    for syllable in all_pinyin.split():
        for tone in [1, 2, 3, 4]:
            pinyin_input = f"{syllable}{tone}"
            pinyin_output = decode_pinyin(pinyin_input)
            entry = plist_entry.format(
                input=pinyin_input,
                output=pinyin_output,
            )
            sys.stdout.write(entry)

    special_cases = [("nv5", "nü"), ("nve5", "nüe"), ("lv5", "lü"), ("lvu5", "lüe")]
    for pinyin_input, pinyin_output in special_cases:
        sys.stdout.write(
            plist_entry.format(
                input=pinyin_input,
                output=pinyin_output,
            )
        )
    sys.stdout.write(plist_template_end)
