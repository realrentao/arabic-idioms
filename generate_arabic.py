#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿拉伯语习语交互式HTML生成器
基于意大利语习语技能模板，适配阿拉伯语RTL排版与文化审美
"""

import os
import json
import hashlib
import base64
import re
from html import escape

# ============================================================
# 数据结构 — 15个阿拉伯语习语
# ============================================================

IDIOMS = [
    {
        "id": 1,
        "idiom": "على راسي",
        "transliteration": "ʿalā rāsī",
        "meaning_cn": "非常乐意效劳 / 定当照办",
        "meaning_ar": "تعبير يعني الاستعداد لفعل أي شيء بكل ترحيب وتكريم، وكأن الطلب يوضع على الرأس تعظيماً له.",
        "meaning_ar_cn": "一种表达方式，表示愿意满怀欢迎和敬意地做任何事，仿佛把请求放在头顶以示尊重。",
        "usage_cn": "用于回应别人的请求或感谢，表达非常乐意帮忙的态度",
        "english_eq": "At your service / With pleasure",
        "cultural_cn": "在阿拉伯文化中，头部是最尊贵的身体部位。说「放在我头上」表示把对方的要求视为最高荣誉。这是黎凡特（沙姆）地区尤其是黎巴嫩、叙利亚、约旦、巴勒斯坦最常用的口语表达之一。",
        "category": "التعابير اليومية",
        "examples": [
            ("أحمد", "بدي مساعدتك في نقل الأثاث.", "我想要你帮忙搬家具。"),
            ("خالد", "على راسي، أنا موجود.", "非常乐意，我随时在。"),
            ("سارة", "شكراً جزيلاً على مساعدتك.", "非常感谢你的帮助。"),
            ("ليلى", "على راسي، هذا واجبي.", "别客气，这是我的本分。")
        ],
        "exercise_q": [
            {"question": "ما معنى تعبير ""على راسي""؟", "options": ["على رأسي / 非常乐意", "على قلبي / 我很悲伤", "على قدمي / 我站着", "على يدي / 我手上"], "answer": "A"}
        ]
    },
    {
        "id": 2,
        "idiom": "نور عيني",
        "transliteration": "nūr ʿaynī",
        "meaning_cn": "我的眼中之光 / 我最珍爱的人",
        "meaning_ar": "تعبير عاطفي يُستخدم للتعبير عن الحب الشديد والتعلق بشخص عزيز جداً، فهو نور العين الذي يُبصر به الإنسان.",
        "meaning_ar_cn": "一种情感表达，用于表达对某个非常珍视之人的强烈的爱与依恋，他/她就是眼睛用以观看的光芒。",
        "usage_cn": "用于称呼深爱的家人、伴侣或孩子，表达深厚的情感",
        "english_eq": "Light of my life / Apple of my eye",
        "cultural_cn": "阿拉伯诗歌中常以「光」比喻至爱之人。在阿拉伯贝都因传统中，「眼中的光」既是视觉的源泉也是灵魂的象征。当代阿拉伯歌曲和影视作品中这个表达极为常见。",
        "category": "المشاعر والمواقف",
        "examples": [
            ("أم", "تعال يا نور عيني، وحشتني.", "过来吧我的宝贝，我想你了。"),
            ("طفل", "ماما، أنا أحبك.", "妈妈，我爱你。"),
            ("أم", "وأنا أحبك أكثر، نور عيني.", "我更爱你，我的宝贝。"),
            ("أب", "بنتي نور عيني وروح قلبي.", "我的女儿是我眼中的光、心中的灵魂。")
        ],
        "exercise_q": [
            {"question": "يكتمل التعبير: ___ ___: ""أنت ___ ___""", "fill": ["نور", "عيني"]}
        ]
    },
    {
        "id": 3,
        "idiom": "طوّل بالك",
        "transliteration": "ṭawwil bālak",
        "meaning_cn": "放长你的心 / 耐心点",
        "meaning_ar": "يعني ""كن صبوراً"" أو ""لا تستعجل""، وفيه إشارة إلى أن الصبر يجلب الراحة، فالقلب الطويل يتحمل المشقة.",
        "meaning_ar_cn": "意思是「要有耐心」或「别着急」，暗示耐心能带来安宁，长心（耐心）能承受困难。",
        "usage_cn": "当对方焦虑或急躁时，劝其冷静耐心等待",
        "english_eq": "Take it easy / Be patient / Hold your horses",
        "cultural_cn": "阿拉伯社会中这个表达体现了「因沙安拉」（如果真主愿意）式的忍耐哲学。中东地区生活节奏与西方不同，这个短语体现了当地人对时间从容不迫的态度，常用于日常交谈中。",
        "category": "التعابير اليومية",
        "examples": [
            ("سائق", "وصلنا؟ طولنا بالطريق!", "到了吗？我们在路上太久了！"),
            ("راكب", "طوّل بالك، وصلنا بعد شوي.", "耐心点，我们一会儿就到了。"),
            ("أم", "الولد لسا ما رد على رسالتي.", "儿子还没回我信息。"),
            ("أب", "طوّل بالك، هو مشغول أكيد.", "别着急，他肯定在忙。")
        ],
        "exercise_q": [
            {"question": "إيش معنى ""طوّل بالك""؟", "options": ["كن صبوراً / 耐心点", "افرح / 高兴点", "امشِ بسرعة / 走快点", "كل كثيراً / 多吃点"], "answer": "A"}
        ]
    },
    {
        "id": 4,
        "idiom": "ألف سلامة",
        "transliteration": "alf salāma",
        "meaning_cn": "一千个平安 / 祝你平安（康复/一路平安）",
        "meaning_ar": "دعاء بالسلامة والحفظ، يُقال عند العودة من السفر أو بعد المرض أو لبس ثوب جديد، وفيه تمني ألف مرة من السلامة.",
        "meaning_ar_cn": "祈求平安和庇护的祝福，在旅行归来、病愈或穿新衣服时说，含有千次平安的祝愿。",
        "usage_cn": "用于祝福病人康复、旅行者平安归来，或祝贺某人穿新衣",
        "english_eq": "Get well soon / Safe travels / Bless you",
        "cultural_cn": "这个表达在阿拉伯世界非常普遍。「一千」在阿拉伯语中常用来表示「很多」，并非确数。当有人从医院出来、旅行归来或穿新衣服时，朋友和亲属都会说「ألف سلامة」。回答通常是「يسلمك」（愿你平安）。",
        "category": "الضيافة والعلاقات",
        "examples": [
            ("زياد", "خرجت من المستشفى اليوم.", "我今天出院了。"),
            ("صديق", "ألف سلامة، الحمد لله على سلامتك.", "祝你平安，感谢真主你平安无恙。"),
            ("مسافر", "وصلت إلى دبي بالسلامة.", "我已平安到达迪拜。"),
            ("أهل", "ألف سلامة، تسلم.", "一路平安，保重。")
        ],
        "exercise_q": [
            {"question": "متى نقول ""ألف سلامة""؟", "options": ["بعد السفر أو المرض / 旅行或病愈后", "عند الغضب / 生气时", "عند الأكل / 吃饭时", "عند النوم / 睡觉时"], "answer": "A"}
        ]
    },
    {
        "id": 5,
        "idiom": "خطفة عين",
        "transliteration": "khaṭfat ʿayn",
        "meaning_cn": "眨眼的功夫 / 一瞬间",
        "meaning_ar": "تعبير عن سرعة حدوث شيء ما، في زمن لا يتجاوز طرفة عين، أي في أسرع وقت ممكن.",
        "meaning_ar_cn": "表示某事发生速度极快的表达，不超过一眨眼的功夫，即尽可能快的时间。",
        "usage_cn": "形容某事发生得极快，或表示很快就回来/完成",
        "english_eq": "In the blink of an eye / In a flash",
        "cultural_cn": "这个表达在阿拉伯语口语中极为常用，尤其是黎凡特地区。它生动地描绘了极短的时间概念。在阿拉伯文学中，时间的短暂常被比作眼睛的动作。",
        "category": "الزمن والعمل",
        "examples": [
            ("موظف", "خلصت الشغل كله؟", "所有工作都做完了？"),
            ("زمل", "أيوا، بخطفة عين.", "是的，一眨眼的功夫。"),
            ("أم", "كبر ولدها بسرعة.", "她儿子长得真快。"),
            ("جارة", "أيوا بخطفة عين صار شباً.", "是啊，一眨眼就成小伙子了。")
        ],
        "exercise_q": [
            {"question": "معنى ""خطفة عين"" هو:", "options": ["بسرعة كبيرة / 非常快", "ببطء / 很慢", "بعيداً / 很远", "قريباً / 很近"], "answer": "A"}
        ]
    },
    {
        "id": 6,
        "idiom": "بين نارين",
        "transliteration": "bayna nārayn",
        "meaning_cn": "在两团火之间 / 进退两难",
        "meaning_ar": "تعبير عن موقف صعب يجد الإنسان نفسه محاصراً بين خيارين غير مرغوبين، كمن يقف بين نارين تحرقه كلتاهما.",
        "meaning_ar_cn": "描述一个人陷入两个都不想要的选项之间的困境，就像站在两团火之间，无论哪边都会被灼伤。",
        "usage_cn": "描述面临困难的抉择，两种选择都不理想",
        "english_eq": "Between a rock and a hard place / Between the devil and the deep blue sea",
        "cultural_cn": "这个表达的意象在世界各文化中都很普遍，但阿拉伯语版本有独特的沙漠文化背景——沙漠中的两团火既不能靠近也不能逃避，极好地象征了困境的本质。",
        "category": "المشاعر والمواقف",
        "examples": [
            ("موظف", "ما بعرف إذا أقبل الوظيفة ولا أبقى.", "我不知道该接受这份工作还是留下。"),
            ("صديق", "أنت بين نارين، الله يعينك.", "你真是进退两难，愿真主帮助你。"),
            ("طالب", "بدرس طب ولا هندسة؟", "学医还是学工程？"),
            ("مرشد", "اختيارك صعب، أنت بين نارين.", "你的选择很难，真是进退两难。")
        ],
        "exercise_q": [
            {"question": "إذا كان الشخص محاصراً بين خيارين سيئين، نقول إنه:", "options": ["بين نارين / 进退两难", "على راسي / 乐意效劳", "نور عيني / 我的宝贝", "على طول / 马上"], "answer": "A"}
        ]
    },
    {
        "id": 7,
        "idiom": "فتح عينيه",
        "transliteration": "fataḥa ʿaynayhi",
        "meaning_cn": "睁开了眼睛 / 恍然大悟",
        "meaning_ar": "يعني أدرك الحقيقة بعد غفلة، أو انتبه إلى أمر كان غافلاً عنه، كمن يفتح عينيه بعد نوم.",
        "meaning_ar_cn": "意思是在疏忽后认识到真相，或注意到之前忽视的事情，如同睡醒后睁开眼睛。",
        "usage_cn": "某人突然明白了一个道理或看穿了真相",
        "english_eq": "Open one's eyes / Wake up to reality",
        "cultural_cn": "阿拉伯谚语说：「眼睛是心灵的窗户」。睁开眼睛这个动作在阿拉伯文化中象征着觉悟和智慧的开启。在很多阿拉伯寓言故事中，主角在经历某些事件后「睁开眼睛」看清了事物的本质。",
        "category": "الحكمة والأمثال",
        "examples": [
            ("شاب", "بعد ما اشتغلت معه، فتحت عيني عليه.", "和他共事后，我看清了他。"),
            ("صديق", "الحمد لله إنك فتحت عينيك.", "感谢真主你终于看清了。"),
            ("أستاذ", "هذه التجربة فتحت عيون الطلاب.", "这个经历让学生们开了眼界。"),
            ("طالب", "صدقت يا أستاذ، فتحت عيوننا.", "老师说得对，您让我们睁开了眼睛。")
        ],
        "exercise_q": [
            {"question": "___ ___ على الحقيقة بعد مدة.", "fill": ["فتح", "عينيه"]}
        ]
    },
    {
        "id": 8,
        "idiom": "عين العقل",
        "transliteration": "ʿayn al-ʿaql",
        "meaning_cn": "智慧之眼 / 理性的视角",
        "meaning_ar": "يقصد به البصيرة والفهم العميق، والنظر إلى الأمور بمنطق وحكمة لا بمجرد الرؤية السطحية.",
        "meaning_ar_cn": "指的是洞察力和深刻的理解，以逻辑和智慧看待事物，而非仅仅停留在表面观察。",
        "usage_cn": "劝人要用理性思考而非冲动行事，要有洞察力",
        "english_eq": "Mind's eye / Insight / Wisdom's perspective",
        "cultural_cn": "阿拉伯哲学传统中，伊本·西那（阿维森纳）和法拉比等哲学家区分了「肉眼」和「智慧之眼」。前者看到表象，后者领悟本质。这个表达在当代阿拉伯语中仍然活跃，用于倡导理性和智慧。",
        "category": "الحكمة والأمثال",
        "examples": [
            ("أب", "لا تاخد قرار متسرع، شوف بعين العقل.", "别仓促做决定，要用智慧之眼看。"),
            ("ابن", "بفكر كويس قبل ما أقرر.", "我会好好想再做决定。"),
            ("صديق", "هي حلوة من برا لكن من جوا لا.", "她外表好看但内在不怎么样。"),
            ("حكيم", "عين العقل تشوف ما لا تراه العين.", "智慧之眼能看到肉眼看不到的东西。")
        ],
        "exercise_q": [
            {"question": "ما معنى ""عين العقل""؟", "options": ["البصيرة والحكمة / 洞察力和智慧", "قوة النظر / 视力好", "جمال العيون / 眼睛漂亮", "مرض العين / 眼病"], "answer": "A"}
        ]
    },
    {
        "id": 9,
        "idiom": "صبر جميل",
        "transliteration": "ṣabr jamīl",
        "meaning_cn": "美好的忍耐 / 优雅地承受",
        "meaning_ar": "الصبر بدون شكوى أو تذمر، والرضا بالقضاء مع الثقة بفرج الله، كما ورد في القرآن الكريم.",
        "meaning_ar_cn": "不抱怨、不诉苦的忍耐，接受命运的安排并相信真主的解脱，正如《古兰经》中所言。",
        "usage_cn": "在遭遇困难时鼓励他人以高尚的方式忍耐，不要抱怨",
        "english_eq": "Beautiful patience / Grace under pressure",
        "cultural_cn": "这个表达直接来自《古兰经》（12:18，12:83），是伊斯兰文化中核心的美德概念。先知雅各布在失去儿子约瑟夫时说：「我只能好好地忍耐。」「美好的忍耐」意味着没有抱怨、没有恼怒、没有对人类失望的忍耐。",
        "category": "المشاعر والمواقف",
        "examples": [
            ("مريض", "العلاج طويل ومتعب.", "治疗又长又累。"),
            ("طبيب", "الله معك، صبر جميل.", "真主与你同在，美好的忍耐。"),
            ("أم", "بعدت عن أولادي سنة كاملة.", "我离开孩子们整整一年了。"),
            ("صديقة", "صبر جميل، والله قريب.", "美好的忍耐，真主很快就让团聚。")
        ],
        "exercise_q": [
            {"question": "وردت عبارة ""صبر جميل"" في:", "options": ["القرآن الكريم / 《古兰经》", "شعر المتنبي / 穆太奈比诗歌", "ألف ليلة / 《一千零一夜》", "الكتاب المقدس / 《圣经》"], "answer": "A"}
        ]
    },
    {
        "id": 10,
        "idiom": "على قد الفراش مد رجليك",
        "transliteration": "ʿalā qadd al-firāsh madd rijlayk",
        "meaning_cn": "量被伸腿 / 量入为出",
        "meaning_ar": "يعني أن يعيش الإنسان ضمن إمكانياته، فلا ينفق أكثر مما يملك، مثل من يمد رجليه بقدر طول فراشه.",
        "meaning_ar_cn": "意思是人要量力而行，花费不超过自己拥有的，就像人按床的长度伸腿一样。",
        "usage_cn": "劝诫人不要超前消费，要在自己的能力范围内生活",
        "english_eq": "Cut your coat according to your cloth / Live within your means",
        "cultural_cn": "这是阿拉伯世界最广为人知的谚语之一，相当于中文的「量入为出」或「看菜吃饭」。在阿拉伯传统社会，节俭和节制被视为美德，这个谚语代代相传。在埃及和沙姆地区有多种变体。",
        "category": "الحكمة والأمثال",
        "examples": [
            ("شاب", "بدي اشتري أغلى سيارة.", "我想买最贵的车。"),
            ("والد", "على قد الفراش مد رجليك، يا ولدي.", "量入为出吧，我的孩子。"),
            ("صديقان", "صار معه ديون لأنه عاش فوق إمكانياته.", "他欠了债因为生活超出了能力范围。"),
            ("صديق", "خلّي يعتبر، على قد الفراش مد رجليك.", "让他吸取教训，要量力而行。")
        ],
        "exercise_q": [
            {"question": "تعبير ""على قد الفراش مد رجليك"" يعني:", "options": ["عِش ضمن إمكانياتك / 量力而行", "نم طويلاً / 睡久一点", "اشتر فراشاً كبيراً / 买大床", "اركض بسرعة / 快跑"], "answer": "A"}
        ]
    },
    {
        "id": 11,
        "idiom": "ميّت تحت الجسر",
        "transliteration": "mayy taḥt al-jisr",
        "meaning_cn": "桥下的水 / 覆水难收，已成过往",
        "meaning_ar": "تعبير عن الأمور التي انتهت ومضت ولا يمكن التراجع عنها أو تغييرها، كالماء الذي جرى تحت الجسر.",
        "meaning_ar_cn": "指已经结束、已经过去且无法挽回或改变的事情，就像桥下流过的水。",
        "usage_cn": "劝人不要纠结于过去的错误或不愉快，要学会放下",
        "english_eq": "Water under the bridge / Let bygones be bygones",
        "cultural_cn": "虽然「桥下的水」这个比喻在英语中也很常见，但阿拉伯版本更强调水已经「死了」（ميّت），带有更强的终结感。这个表达在阿拉伯基督教和穆斯林社区都广泛使用，强调对过去的和解与释怀。",
        "category": "الزمن والعمل",
        "examples": [
            ("صديقان", "لسا زعلان من اللي صار؟", "还在为之前的事生气吗？"),
            ("صديق", "لا، ميّت تحت الجسر، خلص.", "不了，都是过去的事了。"),
            ("زوجان", "نسيتِ المشاكل اللي صارت بينا؟", "你忘了我们之间的那些问题了吗？"),
            ("زوجة", "هذا ميّت تحت الجسر، نبدا من جديد.", "那些都过去了，我们重新开始。")
        ],
        "exercise_q": [
            {"question": "ميّت تحت ___", "fill": ["الجسر"]}
        ]
    },
    {
        "id": 12,
        "idiom": "أهلاً وسهلاً",
        "transliteration": "ahlan wa sahlan",
        "meaning_cn": "家人与坦途 / 热烈欢迎",
        "meaning_ar": "تعبير ترحيبي يعني ""أصبت أهلاً ونزلت سهلاً""، أي صادفت أهلك وأقرباءك ونزلت في مكان سهل مريح.",
        "meaning_ar_cn": "一种欢迎表达，意思是「你遇到了家人和亲人，来到了一个舒适便利的地方」。",
        "usage_cn": "迎接客人、新朋友或表示热烈欢迎时的标准问候语",
        "english_eq": "Welcome / You are among family",
        "cultural_cn": "「أهلاً وسهلاً」是阿拉伯文化中最具代表性的欢迎语，源自阿拉伯游牧传统——热情好客是沙漠生存的关键道德。回答通常是「أهلاً فيك」（你也一样）。在阿拉伯世界，无论贫富，热情接待客人是基本的文化规范。许多阿拉伯家庭入口处都有「أهلاً وسهلاً」的装饰牌。",
        "category": "الضيافة والعلاقات",
        "examples": [
            ("ضيف", "السلام عليكم، أول مرة أجي عندكم.", "你好，我第一次来你们这儿。"),
            ("مضيف", "أهلاً وسهلاً، نورت البيت.", "热烈欢迎，你让寒舍蓬荜生辉。"),
            ("مدير", "هذا زميلنا الجديد من فرنسا.", "这是我们来自法国的新同事。"),
            ("موظفون", "أهلاً وسهلاً فيك، حياك الله.", "热烈欢迎你，欢迎光临。")
        ],
        "exercise_q": [
            {"question": "الرد المناسب على ""أهلاً وسهلاً"" هو:", "options": ["أهلاً فيك / 你也一样", "لا شكر على واجب / 不客气", "مع السلامة / 再见", "إن شاء الله / 如果真主意欲"], "answer": "A"}
        ]
    },
    {
        "id": 13,
        "idiom": "على بالي",
        "transliteration": "ʿalā bālī",
        "meaning_cn": "在我脑海里 / 我记在心里",
        "meaning_ar": "تعبير يعني ""في ذهني"" أو ""أنا متذكر"" أو ""مهتم بالأمر""، ويشير إلى أن الشخص يحمل شيئاً في فكره واهتمامه.",
        "meaning_ar_cn": "表达意思是「在我脑中」或「我记得」或「我在意」，表示某人在思考或关注某事。",
        "usage_cn": "表示记得某事、正在考虑某事，或心里有数",
        "english_eq": "On my mind / I've got it covered / I'll keep it in mind",
        "cultural_cn": "这个表达在阿拉伯语口语中使用频率极高。「بال」一词在古典阿拉伯语中指「心」或「意念」，是精密的内心状态。在不同阿拉伯方言中发音略有不同（如埃及方言说「على بالي」、黎凡特说「على بالي」）。",
        "category": "التعابير اليومية",
        "examples": [
            ("أم", "شريت حاجات البيت؟", "买了家里的东西吗？"),
            ("ابن", "على بالي، أنا جايي فيها.", "我记着呢，我正要去买。"),
            ("سكرتير", "معاد السفر يوم الاثنين.", "旅行时间是周一。"),
            ("موظف", "على بالي، أنا منظم كلشي.", "放心，我来安排一切。")
        ],
        "exercise_q": [
            {"question": "على ___", "fill": ["بالي"]}
        ]
    },
    {
        "id": 14,
        "idiom": "يد بيد",
        "transliteration": "yad bi-yad",
        "meaning_cn": "手牵手 / 齐心协力、团结合作",
        "meaning_ar": "تعبير عن التعاون والتضامن والعمل الجماعي، حيث يكون الجميع متحدين كأن أيديهم متشابكة معاً.",
        "meaning_ar_cn": "表达合作、团结和集体行动，所有人团结一致仿佛手与手交织在一起。",
        "usage_cn": "鼓励团队合作、国家团结或集体行动时的口号或理念",
        "english_eq": "Hand in hand / Together / United we stand",
        "cultural_cn": "「يد بيد」在现代阿拉伯世界中常用作政治口号和社会团结的象征。阿拉伯人有很强的集体主义文化，强调家庭、部落和社区之间的相互支持（العشائرية）。这个表达完美体现了阿拉伯文化中「集体重于个人」的价值观。",
        "category": "الضيافة والعلاقات",
        "examples": [
            ("مدير", "لننجح هذا المشروع، لازم نشتغل يد بيد.", "要成功完成这个项目，我们必须齐心协办。"),
            ("فريق", "نحن معك يا مدير، كلنا يد واحدة.", "我们和你在一起，经理，我们团结一致。"),
            ("قائد", "من أجل بناء المجتمع، يد بيد.", "为了建设社会，齐心协力。"),
            ("متظاهر", "يد بيد نبني الوطن.", "手挽手建设国家。")
        ],
        "exercise_q": [
            {"question": "يد ب ___", "fill": ["يد"]}
        ]
    },
    {
        "id": 15,
        "idiom": "الصديق وقت الضيق",
        "transliteration": "al-ṣadīq waqt al-ḍīq",
        "meaning_cn": "患难见真情 / 困境时才知谁是真正的朋友",
        "meaning_ar": "المقصود أن الصديق الحقيقي يُعرف في الشدائد والمحن، ففي وقت الرخاء الكل أصدقاء، أما في وقت الضيق فيظهر الصديق الحقيقي.",
        "meaning_ar_cn": "意思是真正的朋友在困难和考验中才能被认识，顺境时人人都是朋友，而在困境中真正的朋友才会显现。",
        "usage_cn": "在经历困难后感叹谁是真朋友，或用来提醒珍惜真正的友谊",
        "english_eq": "A friend in need is a friend indeed",
        "cultural_cn": "这句阿拉伯谚语与英语谚语「A friend in need is a friend indeed」几乎完全对应。阿拉伯游牧传统中，沙漠中的同伴关系比血缘关系有时更为重要——在恶劣环境中，一个可靠的朋友可能决定生死。因此友谊在阿拉伯文化中被视为神圣的纽带。",
        "category": "الحكمة والأمثال",
        "examples": [
            ("رجل", "لما كان عندي فلوس، كل الناس حولي.", "我有钱的时候，所有人都在我身边。"),
            ("زوجته", "الحين عرفت إنو الصديق وقت الضيق.", "现在你知道了患难见真情。"),
            ("صديقان", "ساعدني في أحلك الظروف.", "他在我最困难的时候帮了我。"),
            ("صديق", "هذا هو الصديق الحقيقي، وقت الضيق.", "这才是真正的朋友——患难见真情。")
        ],
        "exercise_q": [
            {"question": "يكتمل المثل: ""الصديق وقت ___""", "options": ["الضيق / 困境", "الفرح / 快乐", "الغنى / 富裕", "السفر / 旅行"], "answer": "A"}
        ]
    }
]

CATEGORIES = [
    ("التعابير اليومية", "日常用语"),
    ("المشاعر والمواقف", "情感与处境"),
    ("الحكمة والأمثال", "智慧与谚语"),
    ("الضيافة والعلاقات", "待客与关系"),
    ("الزمن والعمل", "时间与工作"),
]

CATEGORY_MAP = dict(CATEGORIES)

# ============================================================
# CSS 样式 — 阿拉伯风格设计
# ============================================================

INDEX_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Naskh+Arabic:wght@400;700&family=Noto+Sans+SC:wght@300;400;700&family=Readex+Pro:wght@300;400;500;600;700&display=swap');

:root {
    --primary: #1B2A4A;
    --primary-light: #2C4270;
    --gold: #C9A84C;
    --gold-light: #E8D080;
    --gold-dark: #A8882E;
    --teal: #2A6B7F;
    --teal-light: #3D8BA0;
    --sand: #E8D5B7;
    --sand-light: #F5EDE1;
    --burgundy: #6B2D4A;
    --cream: #FEFCF6;
    --text-dark: #1A1A2E;
    --text-light: #F5F0E8;
    --shadow: 0 4px 24px rgba(27,42,74,0.12);
    --radius: 14px;
    --radius-sm: 8px;
    --gold-grad: linear-gradient(135deg, #C9A84C, #E8D080, #C9A84C);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Readex Pro', 'Noto Sans SC', sans-serif;
    background-color: var(--cream);
    color: var(--text-dark);
    direction: rtl;
    line-height: 1.8;
    min-height: 100vh;
}

/* ===== 背景纹饰 ===== */
body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(circle at 15% 20%, rgba(201,168,76,0.04) 0%, transparent 50%),
        radial-gradient(circle at 85% 80%, rgba(27,42,74,0.04) 0%, transparent 50%),
        repeating-linear-gradient(45deg,
            transparent, transparent 20px,
            rgba(201,168,76,0.015) 20px, rgba(201,168,76,0.015) 21px),
        repeating-linear-gradient(-45deg,
            transparent, transparent 20px,
            rgba(27,42,74,0.01) 20px, rgba(27,42,74,0.01) 21px);
    pointer-events: none;
    z-index: 0;
}

/* ===== 顶部装饰条 ===== */
.header-decoration {
    height: 8px;
    background: linear-gradient(90deg, var(--primary), var(--gold), var(--teal), var(--gold), var(--burgundy), var(--gold), var(--primary));
    position: relative;
    z-index: 2;
}

/* ===== Header ===== */
header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 50%, #0F1D35 100%);
    color: var(--cream);
    padding: 40px 20px 50px;
    text-align: center;
    position: relative;
    overflow: hidden;
    z-index: 1;
}

header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; right: -50%; bottom: -50%;
    background:
        radial-gradient(circle at 30% 40%, rgba(201,168,76,0.08) 0%, transparent 40%),
        radial-gradient(circle at 70% 60%, rgba(42,107,127,0.06) 0%, transparent 40%);
    animation: headerGlow 15s ease-in-out infinite alternate;
}

@keyframes headerGlow {
    0% { transform: translate(0, 0); }
    100% { transform: translate(-3%, -5%); }
}

/* 伊斯兰几何纹样 */
header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 40px;
    background:
        linear-gradient(135deg, var(--gold) 4px, transparent 4px) 0 0,
        linear-gradient(225deg, var(--gold) 4px, transparent 4px) 0 0;
    background-size: 14px 14px;
    background-color: transparent;
    opacity: 0.35;
}

header h1 {
    font-family: 'Amiri', serif;
    font-size: 2.8rem;
    font-weight: 700;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 12px rgba(0,0,0,0.3);
    margin-bottom: 6px;
    letter-spacing: 1px;
}

header h1 .gold {
    color: var(--gold);
}

header .subtitle {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 1.1rem;
    opacity: 0.85;
    position: relative;
    z-index: 1;
    letter-spacing: 2px;
}

header .arabic-deco {
    font-family: 'Amiri', serif;
    font-size: 1.4rem;
    color: var(--gold-light);
    opacity: 0.4;
    margin-top: 8px;
    letter-spacing: 8px;
    position: relative;
    z-index: 1;
}

/* ===== 星星装饰 ===== */
.star-decoration {
    display: flex;
    justify-content: center;
    gap: 12px;
    margin: 10px 0;
    position: relative;
    z-index: 1;
}

.star-decoration span {
    display: inline-block;
    color: var(--gold);
    font-size: 0.9rem;
    opacity: 0.5;
}

/* ===== 搜索与分类区域 ===== */
.controls-panel {
    position: relative;
    z-index: 2;
    max-width: 1000px;
    margin: -25px auto 30px;
    background: white;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px 30px;
    border: 1px solid rgba(201,168,76,0.2);
}

.search-container {
    display: flex;
    gap: 12px;
    margin-bottom: 18px;
}

.search-container input {
    flex: 1;
    padding: 14px 20px;
    border: 2px solid #E8E0D0;
    border-radius: var(--radius-sm);
    font-size: 1rem;
    font-family: 'Readex Pro', 'Noto Sans SC', sans-serif;
    direction: rtl;
    background: var(--sand-light);
    color: var(--text-dark);
    transition: all 0.3s;
    outline: none;
}

.search-container input:focus {
    border-color: var(--gold);
    background: white;
    box-shadow: 0 0 0 4px rgba(201,168,76,0.15);
}

.search-container input::placeholder {
    color: #999;
    font-size: 0.9rem;
}

#searchCount {
    display: flex;
    align-items: center;
    padding: 0 8px;
    font-size: 0.85rem;
    color: #999;
    white-space: nowrap;
}

.category-filters {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.category-filters button {
    padding: 8px 18px;
    border: 1.5px solid var(--primary);
    border-radius: 40px;
    background: transparent;
    color: var(--primary);
    font-size: 0.85rem;
    font-family: 'Readex Pro', 'Noto Sans SC', sans-serif;
    cursor: pointer;
    transition: all 0.3s;
    direction: rtl;
}

.category-filters button:hover {
    background: rgba(27,42,74,0.06);
    border-color: var(--gold);
    color: var(--gold-dark);
}

.category-filters button.active {
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    color: white;
    border-color: var(--primary);
    box-shadow: 0 2px 12px rgba(27,42,74,0.2);
}

.category-filters button.all-btn {
    border-color: var(--gold);
    color: var(--gold-dark);
    font-weight: 500;
}

.category-filters button.all-btn.active {
    background: var(--gold-grad);
    color: white;
    border-color: var(--gold);
}

/* ===== 习语网格 ===== */
.idiom-grid {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px 60px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 24px;
    position: relative;
    z-index: 1;
}

.idiom-card {
    background: white;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px 24px;
    text-decoration: none;
    color: var(--text-dark);
    transition: all 0.4s cubic-bezier(.25,.1,.25,1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    border: 1px solid rgba(201,168,76,0.12);
}

.idiom-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(27,42,74,0.18);
    border-color: var(--gold);
}

/* 卡片顶部装饰线 */
.idiom-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--gold), var(--teal), var(--gold));
    opacity: 0;
    transition: opacity 0.3s;
}

.idiom-card:hover::before {
    opacity: 1;
}

/* 阿拉伯纹饰背景 */
.idiom-card::after {
    content: '✦';
    position: absolute;
    top: -8px; left: -8px;
    font-size: 4rem;
    color: rgba(201,168,76,0.04);
    line-height: 1;
    pointer-events: none;
}

.idiom-card .idiom-ar {
    font-family: 'Amiri', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 4px;
    line-height: 1.4;
}

.idiom-card .idiom-trans {
    font-size: 0.8rem;
    color: var(--teal);
    font-style: italic;
    margin-bottom: 8px;
    direction: ltr;
    text-align: left;
}

.idiom-card .idiom-cn {
    font-size: 0.95rem;
    color: #666;
    margin-bottom: 12px;
}

.idiom-card .idiom-category {
    display: inline-block;
    padding: 4px 14px;
    background: linear-gradient(135deg, var(--sand-light), var(--sand));
    border-radius: 40px;
    font-size: 0.75rem;
    color: var(--primary);
    margin-top: auto;
    align-self: flex-start;
    border: 1px solid rgba(27,42,74,0.08);
}

.idiom-card .card-number {
    position: absolute;
    top: 12px;
    left: 16px;
    font-size: 2.3rem;
    font-weight: 700;
    color: rgba(27,42,74,0.06);
    line-height: 1;
    font-family: 'Amiri', serif;
}

/* ===== 页脚 ===== */
footer {
    background: var(--primary);
    color: var(--cream);
    text-align: center;
    padding: 30px 20px;
    position: relative;
    font-size: 0.85rem;
    opacity: 0.8;
}

footer::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 6px;
    background: var(--gold-grad);
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
    header h1 { font-size: 2rem; }
    header .subtitle { font-size: 0.95rem; }
    header .arabic-deco { font-size: 1rem; }
    .controls-panel { margin: -20px 10px 20px; padding: 18px 16px; }
    .idiom-grid { grid-template-columns: 1fr; padding: 0 12px 40px; gap: 16px; }
    .idiom-card { padding: 20px 18px; }
    .idiom-card .idiom-ar { font-size: 1.3rem; }
    .category-filters { gap: 6px; }
    .category-filters button { font-size: 0.78rem; padding: 6px 14px; }
    .search-container { flex-direction: column; gap: 8px; }
    #searchCount { padding: 0; }
}

@media (min-width: 769px) and (max-width: 1024px) {
    .idiom-grid { grid-template-columns: repeat(2, 1fr); }
}
"""

IDIOM_PAGE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Naskh+Arabic:wght@400;700&family=Noto+Sans+SC:wght@300;400;700&family=Readex+Pro:wght@300;400;500;600;700&display=swap');

:root {
    --primary: #1B2A4A;
    --primary-light: #2C4270;
    --gold: #C9A84C;
    --gold-light: #E8D080;
    --gold-dark: #A8882E;
    --teal: #2A6B7F;
    --teal-light: #3D8BA0;
    --sand: #E8D5B7;
    --sand-light: #F5EDE1;
    --burgundy: #6B2D4A;
    --cream: #FEFCF6;
    --text-dark: #1A1A2E;
    --text-light: #F5F0E8;
    --shadow: 0 4px 24px rgba(27,42,74,0.12);
    --radius: 14px;
    --radius-sm: 8px;
    --gold-grad: linear-gradient(135deg, #C9A84C, #E8D080, #C9A84C);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Readex Pro', 'Noto Sans SC', sans-serif;
    background-color: var(--cream);
    color: var(--text-dark);
    direction: rtl;
    line-height: 1.8;
    min-height: 100vh;
}

body::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(circle at 15% 20%, rgba(201,168,76,0.04) 0%, transparent 50%),
        radial-gradient(circle at 85% 80%, rgba(27,42,74,0.04) 0%, transparent 50%),
        repeating-linear-gradient(45deg,
            transparent, transparent 20px,
            rgba(201,168,76,0.015) 20px, rgba(201,168,76,0.015) 21px),
        repeating-linear-gradient(-45deg,
            transparent, transparent 20px,
            rgba(27,42,74,0.01) 20px, rgba(27,42,74,0.01) 21px);
    pointer-events: none;
    z-index: 0;
}

/* ===== 导航栏 ===== */
.top-bar {
    background: var(--primary);
    padding: 12px 24px;
    display: flex;
    align-items: center;
    gap: 16px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 16px rgba(0,0,0,0.2);
}

.top-bar a {
    color: var(--cream);
    text-decoration: none;
    font-size: 0.9rem;
    opacity: 0.85;
    transition: opacity 0.3s;
    display: flex;
    align-items: center;
    gap: 6px;
}

.top-bar a:hover { opacity: 1; }

.top-bar .nav-title {
    font-family: 'Amiri', serif;
    color: var(--gold);
    font-size: 1rem;
    margin-right: auto;
}

.top-bar .nav-counter {
    background: rgba(201,168,76,0.2);
    color: var(--gold);
    padding: 2px 14px;
    border-radius: 20px;
    font-size: 0.78rem;
}

/* ===== 顶部装饰条 ===== */
.header-decoration {
    height: 6px;
    background: linear-gradient(90deg, var(--primary), var(--gold), var(--teal), var(--gold), var(--burgundy), var(--gold), var(--primary));
}

/* ===== 主内容区 ===== */
.container {
    max-width: 900px;
    margin: 0 auto;
    padding: 30px 20px 60px;
    position: relative;
    z-index: 1;
}

/* ===== 习语标题区块 ===== */
.idiom-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    border-radius: var(--radius);
    padding: 36px 32px;
    text-align: center;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(27,42,74,0.2);
}

.idiom-header::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; right: -50%; bottom: -50%;
    background:
        radial-gradient(circle at 30% 30%, rgba(201,168,76,0.06) 0%, transparent 40%),
        radial-gradient(circle at 70% 70%, rgba(42,107,127,0.04) 0%, transparent 40%);
}

.idiom-header .idiom-ar {
    font-family: 'Amiri', serif;
    font-size: 2.8rem;
    color: var(--gold-light);
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 16px rgba(0,0,0,0.3);
    line-height: 1.4;
}

.idiom-header .idiom-trans {
    font-size: 0.95rem;
    color: var(--teal-light);
    margin-top: 6px;
    direction: ltr;
    text-align: center;
    position: relative;
    z-index: 1;
    font-style: italic;
}

.idiom-header .idiom-cn {
    font-size: 1.2rem;
    color: var(--sand);
    margin-top: 10px;
    position: relative;
    z-index: 1;
    letter-spacing: 1px;
}

.idiom-header .idiom-en {
    font-size: 0.85rem;
    color: rgba(245,240,232,0.6);
    margin-top: 4px;
    position: relative;
    z-index: 1;
    direction: ltr;
}

.idiom-header .play-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 16px;
    padding: 10px 28px;
    background: var(--gold-grad);
    border: none;
    border-radius: 40px;
    color: var(--primary);
    font-size: 0.9rem;
    font-family: 'Readex Pro', sans-serif;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s;
    position: relative;
    z-index: 1;
}

.idiom-header .play-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 20px rgba(201,168,76,0.4);
}

.idiom-header .play-btn:active { transform: scale(0.97); }

.idiom-header .play-btn .icon {
    font-size: 1.2rem;
}

/* ===== 语速控制 ===== */
.speed-control {
    position: relative;
    z-index: 1;
    margin-top: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.speed-control label {
    color: rgba(245,240,232,0.7);
    font-size: 0.8rem;
}

.speed-control button {
    padding: 4px 14px;
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 20px;
    background: transparent;
    color: var(--sand);
    font-size: 0.78rem;
    cursor: pointer;
    transition: all 0.3s;
    font-family: 'Readex Pro', sans-serif;
}

.speed-control button:hover {
    background: rgba(201,168,76,0.15);
    border-color: var(--gold);
}

.speed-control button.active {
    background: var(--gold-grad);
    color: var(--primary);
    border-color: var(--gold);
    font-weight: 600;
}

/* ===== 分类标签 ===== */
.idiom-category-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 18px;
    background: linear-gradient(135deg, var(--sand-light), var(--sand));
    border-radius: 40px;
    font-size: 0.8rem;
    color: var(--primary);
    border: 1px solid rgba(27,42,74,0.1);
    margin-bottom: 20px;
}

/* ===== 章节卡片 ===== */
.section {
    background: white;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px 30px;
    margin-bottom: 24px;
    border: 1px solid rgba(201,168,76,0.1);
}

.section-title {
    font-family: 'Amiri', serif;
    font-size: 1.3rem;
    color: var(--primary);
    margin-bottom: 16px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--sand);
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title .gold-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: var(--gold);
    border-radius: 50%;
    flex-shrink: 0;
}

/* ===== 含义区块 ===== */
.meaning-content {
    padding: 4px 0;
}

.meaning-content .ar-text {
    font-family: 'Amiri', serif;
    font-size: 1.1rem;
    line-height: 1.9;
    color: var(--text-dark);
    margin-bottom: 10px;
}

.meaning-content .trans-text {
    color: #888;
    font-size: 0.9rem;
    padding-right: 20px;
    border-right: 3px solid var(--gold);
    margin-bottom: 10px;
}

.meaning-content .toggle-trans {
    color: var(--teal);
    cursor: pointer;
    font-size: 0.82rem;
    user-select: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.meaning-content .toggle-trans:hover { opacity: 0.7; }

/* ===== 用法说明 ===== */
.usage-box {
    background: linear-gradient(135deg, rgba(27,42,74,0.03), rgba(42,107,127,0.03));
    border: 1px solid rgba(201,168,76,0.15);
    border-radius: var(--radius-sm);
    padding: 16px 18px;
    margin-top: 12px;
}

.usage-box .usage-label {
    font-size: 0.8rem;
    color: var(--gold-dark);
    font-weight: 600;
    margin-bottom: 4px;
}

.usage-box .usage-text {
    font-size: 0.92rem;
    color: #666;
}

/* ===== 文化注释 ===== */
.cultural-box {
    background: linear-gradient(135deg, rgba(42,107,127,0.04), rgba(201,168,76,0.04));
    border: 1px solid rgba(42,107,127,0.12);
    border-radius: var(--radius-sm);
    padding: 16px 18px;
    margin-top: 4px;
}

.cultural-box .cultural-label {
    font-size: 0.8rem;
    color: var(--teal);
    font-weight: 600;
    margin-bottom: 4px;
}

.cultural-box .cultural-text {
    font-size: 0.9rem;
    color: #555;
    line-height: 1.9;
}

/* ===== 例句区块 ===== */
.examples-list {
    list-style: none;
}

.example-item {
    display: flex;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px dashed #F0EAE0;
}

.example-item:last-child { border-bottom: none; }

.example-item .speaker {
    font-weight: 600;
    color: var(--teal);
    font-size: 0.85rem;
    min-width: 50px;
    flex-shrink: 0;
    padding-top: 2px;
}

.example-item .speech {
    flex: 1;
    min-width: 0;
}

.example-item .speech .ar-speech {
    font-family: 'Amiri', serif;
    font-size: 1rem;
    color: var(--text-dark);
    display: inline;
}

.example-item .speech .cn-speech {
    color: #888;
    font-size: 0.85rem;
    margin-top: 2px;
    padding-right: 12px;
    display: block;
}

.example-item .play-ex-btn {
    background: none;
    border: none;
    color: var(--gold-dark);
    width: 22px;
    height: 22px;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 0.65rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    vertical-align: middle;
    margin-right: 6px;
    opacity: 0.6;
}

.example-item .play-ex-btn:hover {
    opacity: 1;
    background: rgba(201,168,76,0.12);
}

/* ===== 含义播放按钮 ===== */
.play-meaning-btn {
    background: none;
    border: 1.5px solid var(--teal);
    color: var(--teal);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.3s;
    font-size: 0.85rem;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-top: 4px;
}

.play-meaning-btn:hover {
    background: var(--teal);
    color: white;
    border-color: var(--teal);
}

/* ===== 练习区块 ===== */
.exercise-block {
    margin-top: 20px;
}

.exercise-block .exercise {
    background: var(--sand-light);
    border-radius: var(--radius-sm);
    padding: 18px;
    margin-bottom: 14px;
    border: 1px solid rgba(201,168,76,0.12);
}

.exercise .ex-question {
    font-family: 'Amiri', serif;
    font-size: 1rem;
    color: var(--primary);
    margin-bottom: 12px;
    line-height: 1.7;
}

.exercise .ex-input {
    padding: 8px 14px;
    border: 2px solid #DDD;
    border-radius: 6px;
    font-family: 'Amiri', serif;
    font-size: 1rem;
    width: 120px;
    direction: rtl;
    outline: none;
    transition: border-color 0.3s;
    margin: 0 2px;
}

.exercise .ex-input:focus {
    border-color: var(--gold);
    box-shadow: 0 0 0 3px rgba(201,168,76,0.12);
}

.exercise .ex-options {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.exercise .ex-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    border: 2px solid #E0D8CC;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all 0.3s;
    background: white;
}

.exercise .ex-option:hover {
    border-color: var(--gold);
    background: rgba(201,168,76,0.04);
}

.exercise .ex-option input[type="radio"] {
    appearance: none;
    width: 18px;
    height: 18px;
    border: 2px solid #CCC;
    border-radius: 50%;
    position: relative;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.3s;
}

.exercise .ex-option input[type="radio"]:checked {
    border-color: var(--gold);
    background: var(--gold);
    box-shadow: inset 0 0 0 4px white;
}

.exercise .ex-option .option-label {
    font-family: 'Amiri', serif;
    font-size: 0.95rem;
}

.exercise .ex-btn {
    margin-top: 12px;
    padding: 8px 24px;
    background: var(--gold-grad);
    border: none;
    border-radius: var(--radius-sm);
    color: var(--primary);
    font-weight: 600;
    font-family: 'Readex Pro', 'Noto Sans SC', sans-serif;
    cursor: pointer;
    transition: all 0.3s;
}

.exercise .ex-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(201,168,76,0.3);
}

.exercise .ex-btn:active { transform: translateY(0); }

.exercise .ex-feedback {
    margin-top: 10px;
    padding: 10px 14px;
    border-radius: var(--radius-sm);
    font-size: 0.9rem;
    display: none;
}

.exercise .ex-feedback.correct {
    display: block;
    background: #E8F5E9;
    color: #2E7D32;
    border: 1px solid #A5D6A7;
}

.exercise .ex-feedback.wrong {
    display: block;
    background: #FFF3E0;
    color: #E65100;
    border: 1px solid #FFCC80;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
    .container { padding: 16px 10px 40px; }
    .idiom-header { padding: 24px 18px; }
    .idiom-header .idiom-ar { font-size: 2rem; }
    .idiom-header .idiom-cn { font-size: 1rem; }
    .section { padding: 18px 16px; }
    .section-title { font-size: 1.1rem; }
    .example-item { flex-direction: column; gap: 4px; }
    .example-item .speaker { min-width: auto; }
    .top-bar { padding: 10px 14px; }
    .exercise .ex-input { width: 90px; }
}

@media (max-width: 480px) {
    .idiom-header .idiom-ar { font-size: 1.6rem; }
}
"""

# ============================================================
# 生成器函数
# ============================================================

def safe_filename(text):
    """生成URL安全的base64文件名（与意大利语技能一致）"""
    h = hashlib.sha256(text.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(h[:12]).decode('utf-8').rstrip('=')

def generate_index_html():
    """生成导航页面"""
    cats_html = ""
    for cat_ar, cat_cn in CATEGORIES:
        cats_html += f"""<button data-category="{escape(cat_ar)}">{escape(cat_ar)}<br><small style="font-weight:400;font-size:0.7rem;opacity:0.7">{escape(cat_cn)}</small></button>\n"""

    cards_html = ""
    for idiom in IDIOMS:
        cat_ar = idiom["category"]
        cat_cn = CATEGORY_MAP.get(cat_ar, "")
        cards_html += f"""
        <a href="idiom-{idiom['id']:02d}.html" class="idiom-card" data-category="{escape(cat_ar)}" data-search="{escape(idiom['idiom'])} {escape(idiom['meaning_cn'])} {escape(idiom['transliteration'])}">
            <span class="card-number">{idiom['id']:02d}</span>
            <div class="idiom-ar">{escape(idiom['idiom'])}</div>
            <div class="idiom-trans">{escape(idiom['transliteration'])}</div>
            <div class="idiom-cn">{escape(idiom['meaning_cn'])}</div>
            <div class="idiom-category">{escape(cat_ar)} · {escape(cat_cn)}</div>
        </a>"""

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>الأمثال العربية · 阿拉伯语习语学习</title>
<style>{INDEX_CSS}</style>
</head>
<body>

<div class="header-decoration"></div>

<header>
    <div class="star-decoration">
        <span>✦</span><span>❋</span><span>✦</span><span>❋</span><span>✦</span>
    </div>
    <h1>الأمثال <span class="gold">العربية</span></h1>
    <div class="subtitle">阿拉伯语习语 · 交互式学习</div>
    <div class="arabic-deco">بسم الله الرحمن الرحيم</div>
</header>

<div class="controls-panel">
    <div class="search-container">
        <input type="text" id="searchInput" placeholder="ابحث عن المثل... 搜索习语..." oninput="filterIdioms()">
        <span id="searchCount">15 / 15</span>
    </div>
    <div class="category-filters">
        <button class="all-btn active" data-category="all" onclick="filterByCategory('all', this)">الكل · 全部</button>
        {cats_html}
    </div>
</div>

<div class="idiom-grid" id="idiomGrid">
    {cards_html}
</div>

<footer>
    <div>الأمثال العربية · 阿拉伯语习语学习</div>
    <div style="margin-top:6px;font-size:0.75rem;opacity:0.6">交互式教学 · 15个常用习语 · RTL 排版</div>
</footer>

<script>
function filterIdioms() {{
    const q = document.getElementById('searchInput').value.trim().toLowerCase();
    const cards = document.querySelectorAll('.idiom-card');
    let count = 0;
    cards.forEach(c => {{
        const searchData = c.getAttribute('data-search').toLowerCase();
        const match = !q || searchData.includes(q);
        c.style.display = match ? '' : 'none';
        if (match) count++;
    }});
    document.getElementById('searchCount').textContent = count + ' / ' + cards.length;
}}

function filterByCategory(cat, btn) {{
    document.querySelectorAll('.category-filters button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cards = document.querySelectorAll('.idiom-card');
    let count = 0;
    cards.forEach(c => {{
        if (cat === 'all' || c.getAttribute('data-category') === cat) {{
            c.style.display = '';
            count++;
        }} else {{
            c.style.display = 'none';
        }}
    }});
    document.getElementById('searchCount').textContent = count + ' / ' + cards.length;
    document.getElementById('searchInput').value = '';
}}
</script>

</body>
</html>"""
    return html


def generate_idiom_page(idiom):
    """生成单个习语详情页"""
    i = idiom
    cat_cn = CATEGORY_MAP.get(i["category"], "")

    # 例句
    examples_html = ""
    for idx, (speaker, ar_text, cn_text) in enumerate(i["examples"]):
        examples_html += f"""
        <li class="example-item">
            <span class="speaker">{escape(speaker)}</span>
            <div class="speech">
                <div class="ar-speech">{escape(ar_text)} <button class="play-ex-btn" onclick="playExample({idx})" title="播放">▶</button></div>
                <div class="cn-speech">{escape(cn_text)}</div>
            </div>
        </li>"""

    # 练习题
    exercises_html = ""
    for ex_idx, ex in enumerate(i["exercise_q"]):
        ex_id = f"ex-{i['id']}-{ex_idx}"
        if "options" in ex:
            opts_html = ""
            for opt_idx, opt in enumerate(ex["options"]):
                letter = chr(65 + opt_idx)
                opts_html += f"""
                <label class="ex-option">
                    <input type="radio" name="{ex_id}" value="{letter}">
                    <span class="option-label">{escape(opt)}</span>
                </label>"""
            exercises_html += f"""
            <div class="exercise">
                <div class="ex-question">{escape(ex["question"])}</div>
                <div class="ex-options">{opts_html}</div>
                <button class="ex-btn" onclick="checkChoice('{ex_id}','{escape(ex["answer"])}')">تحقق · 检查</button>
                <div class="ex-feedback" id="fb-{ex_id}"></div>
            </div>"""
        elif "fill" in ex:
            # 填空题：用 ___ 标记空位
            q_text = ex["question"]
            parts = ex["fill"]
            fill_html = ""
            for fi_idx, _ in enumerate(parts):
                fill_html += f"""<input class="ex-input" id="fill-{ex_id}-{fi_idx}" type="text" placeholder="…" autocomplete="off" oninput="clearFillFeedback('{ex_id}')">"""
            exercises_html += f"""
            <div class="exercise">
                <div class="ex-question">{escape(q_text)}</div>
                <div>{fill_html}</div>
                <button class="ex-btn" onclick="checkFill('{ex_id}', {json.dumps(parts)})">تحقق · 检查</button>
                <div class="ex-feedback" id="fb-{ex_id}"></div>
                <button class="ex-btn" style="background:transparent;border:1px solid var(--teal);color:var(--teal);margin-right:8px" onclick="showFillAnswer('{ex_id}', {json.dumps(parts)})">إظهار الإجابة · 显示答案</button>
            </div>"""

    # ---- 读取音频内联数据 ----
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    iid = i["id"]

    main_b64 = ""
    main_json_path = os.path.join(data_dir, f"idiom-{iid:02d}-audio-main.json")
    if os.path.exists(main_json_path):
        with open(main_json_path, "r", encoding="utf-8") as f:
            main_b64 = json.load(f)["audio"]

    # 含义音频
    meaning_b64 = ""
    meaning_mp3 = f"audio/{safe_filename(i['meaning_ar'])}.mp3"
    meaning_json_path = os.path.join(data_dir, f"idiom-{iid:02d}-audio-meaning.json")
    if os.path.exists(meaning_json_path):
        with open(meaning_json_path, "r", encoding="utf-8") as f:
            meaning_b64 = json.load(f)["audio"]

    ex_b64_list = []
    ex_mp3_list = []
    for ex_idx in range(len(i["examples"])):
        ex_text = i["examples"][ex_idx][1]
        ex_mp3_list.append(f"audio/{safe_filename(ex_text)}.mp3")
        ex_json_path = os.path.join(data_dir, f"idiom-{iid:02d}-audio-ex-{ex_idx}.json")
        if os.path.exists(ex_json_path):
            with open(ex_json_path, "r", encoding="utf-8") as f:
                ex_b64_list.append(json.load(f)["audio"])
        else:
            ex_b64_list.append("")

    html = f"""<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(i['idiom'])} · 阿拉伯语习语</title>
<style>{IDIOM_PAGE_CSS}</style>
</head>
<body>

<div class="top-bar">
    <a href="index.html">← العودة · 返回</a>
    <div class="nav-counter">{i['id']:02d} / 15</div>
    <div class="nav-title">الأمثال العربية</div>
</div>

<div class="header-decoration"></div>

<div class="container">

    <div class="idiom-category-tag">{escape(i['category'])} · {escape(cat_cn)}</div>

    <div class="idiom-header">
        <div class="idiom-ar">{escape(i['idiom'])}</div>
        <div class="idiom-trans">{escape(i['transliteration'])}</div>
        <div class="idiom-cn">{escape(i['meaning_cn'])}</div>
        <div class="idiom-en">{escape(i['english_eq'])}</div>
        <button class="play-btn" onclick="playMainAudio()"><span class="icon">▶</span> استمع · 听发音</button>
        <div class="speed-control">
            <label>السرعة · 语速:</label>
            <button onclick="setSpeed(0.6)" data-speed="0.6">0.6×</button>
            <button onclick="setSpeed(1.0)" class="active" data-speed="1.0">1.0×</button>
            <button onclick="setSpeed(1.4)" data-speed="1.4">1.4×</button>
        </div>
    </div>

    <!-- 含义 -->
    <div class="section">
        <div class="section-title"><span class="gold-dot"></span> المعنى · 含义</div>
        <div class="meaning-content">
            <div class="ar-text" style="display:flex;align-items:flex-start;gap:10px;">
                <span>{escape(i['meaning_ar'])}</span>
                <button class="play-meaning-btn" onclick="playMeaningAudio()" title="播放含义发音">▶</button>
            </div>
            <div class="trans-text" id="meaningTrans">{escape(i['meaning_ar_cn'])}</div>
        </div>
        <div class="usage-box">
            <div class="usage-label">الاستخدام · 用法</div>
            <div class="usage-text">{escape(i['usage_cn'])}</div>
        </div>
    </div>

    <!-- 文化注释 -->
    <div class="section">
        <div class="section-title"><span class="gold-dot"></span> الخلفية الثقافية · 文化背景</div>
        <div class="cultural-box">
            <div class="cultural-text">{escape(i['cultural_cn'])}</div>
        </div>
    </div>

    <!-- 例句 -->
    <div class="section">
        <div class="section-title"><span class="gold-dot"></span> أمثلة · 例句</div>
        <ul class="examples-list">
            {examples_html}
        </ul>
    </div>

    <!-- 练习 -->
    <div class="section">
        <div class="section-title"><span class="gold-dot"></span> تمرين · 练习</div>
        <div class="exercise-block">
            {exercises_html}
        </div>
    </div>

</div>

<footer>
    <div>{escape(i['idiom'])} · {escape(i['meaning_cn'])}</div>
    <div style="margin-top:6px;font-size:0.75rem;opacity:0.6">عود إلى <a href="index.html" style="color:var(--gold);">الصفحة الرئيسية · 首页</a></div>
</footer>

<script>
// ===== 音频系统（内联base64，无需fetch）=====
let playbackSpeed = 1.0;

// 内联音频数据
const MAIN_AUDIO_B64 = "{escape(main_b64)}";
const MEANING_AUDIO_B64 = "{escape(meaning_b64)}";
const MEANING_AUDIO_MP3 = "{escape(meaning_mp3)}";
const EX_AUDIO_B64 = [{", ".join(f'"{escape(b)}"' for b in ex_b64_list)}];
const EX_AUDIO_MP3 = [{", ".join(f'"{escape(f)}"' for f in ex_mp3_list)}];

function playMainAudio() {{
    playAudioWithFallback('audio/{safe_filename(i["idiom"])}.mp3', MAIN_AUDIO_B64);
}}

function playExample(idx) {{
    playAudioWithFallback(EX_AUDIO_MP3[idx], EX_AUDIO_B64[idx]);
}}

function playAudioWithFallback(mp3Path, b64data) {{
    const audio = new Audio(mp3Path);
    audio.playbackRate = playbackSpeed;
    audio.onerror = function() {{
        if (b64data) {{
            const a = new Audio('data:audio/mpeg;base64,' + b64data);
            a.playbackRate = playbackSpeed;
            a.play().catch(e => console.warn('音频播放失败（备用）:', e));
        }} else {{
            console.warn('无可用音频数据:', mp3Path);
        }}
    }};
    audio.play().catch(function() {{
        // 首次播放失败，触发 onerror 走备用
    }});
}}

function playMeaningAudio() {{
    playAudioWithFallback(MEANING_AUDIO_MP3, MEANING_AUDIO_B64);
}}

function setSpeed(speed) {{
    playbackSpeed = speed;
    document.querySelectorAll('.speed-control button').forEach(b => {{
        b.classList.toggle('active', parseFloat(b.dataset.speed) === speed);
    }});
}}

// ===== 练习检查 =====
function clearFillFeedback(name) {{
    const fb = document.getElementById('fb-' + name);
    fb.className = 'ex-feedback';
    // 重置所有输入框边框
    const inputs = document.querySelectorAll('[id^="fill-' + name + '"]');
    inputs.forEach(inp => inp.style.borderColor = '#DDD');
}}
function checkChoice(name, correct) {{
    const selected = document.querySelector('input[name="' + name + '"]:checked');
    const fb = document.getElementById('fb-' + name);
    if (!selected) {{
        fb.className = 'ex-feedback wrong';
        fb.textContent = '⚠️ الرجاء اختيار إجابة · 请选择一个选项';
        return;
    }}
    if (selected.value === correct) {{
        fb.className = 'ex-feedback correct';
        fb.textContent = '✅ صحيح! · 正确！';
    }} else {{
        fb.className = 'ex-feedback wrong';
        fb.textContent = '❌ خطأ · 不正确，再试一次';
    }}
}}

function checkFill(name, answers) {{
    const fb = document.getElementById('fb-' + name);
    let allCorrect = true;

    // 阿拉伯语归一化：去变音符 + 统一字母变体 + 去空/标点
    function normalizeArabic(s) {{
        let t = s;
        // 1) 去掉变音符号 (tashkeel): fatha, kasra, damma, sukun, shadda, madd, etc.
        t = t.replace(/[\u064B-\u065F\u0670]/g, '');
        // 2) 统一 alif 变体 → 裸 alif
        t = t.replace(/[آأإٱ]/g, 'ا');
        // 3) 统一 teh marbuta → heh
        t = t.replace(/ة/g, 'ه');
        // 4) 统一 alif maksura → ya
        t = t.replace(/ى/g, 'ي');
        // 5) 去空白 + 标点
        t = t.replace(/[\\s،؟!.;:,()()\"\"']/g, '');
        return t;
    }}

    answers.forEach((ans, i) => {{
        const input = document.getElementById('fill-' + name + '-' + i);
        const userVal = input.value.trim();
        if (normalizeArabic(userVal) !== normalizeArabic(ans)) {{
            allCorrect = false;
            input.style.borderColor = '#E65100';
        }} else {{
            input.style.borderColor = '#4CAF50';
        }}
    }});
    if (allCorrect) {{
        fb.className = 'ex-feedback correct';
        fb.textContent = '✅ صحيح! كل الإجابات صحيحة · 全部正确！';
    }} else {{
        fb.className = 'ex-feedback wrong';
        fb.textContent = '❌ خطأ · 还有错误，再试一次';
    }}
}}

function showFillAnswer(name, answers) {{
    answers.forEach((ans, i) => {{
        const input = document.getElementById('fill-' + name + '-' + i);
        input.value = ans;
        input.style.borderColor = '#4CAF50';
    }});
    const fb = document.getElementById('fb-' + name);
    fb.className = 'ex-feedback correct';
    fb.textContent = '💡 الإجابة الصحيحة · 正确答案已显示';
}}
</script>

</body>
</html>"""
    return html


def generate_all():
    """完整生成所有页面"""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 生成 index.html
    index_html = generate_index_html()
    with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print(f"✅ 已生成: index.html")

    # 生成每个习语详情页
    for idiom in IDIOMS:
        page_html = generate_idiom_page(idiom)
        filename = f"idiom-{idiom['id']:02d}.html"
        with open(os.path.join(base_dir, filename), "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"✅ 已生成: {filename}")

    print(f"\n🎉 完成！共生成 {len(IDIOMS) + 1} 个 HTML 页面。")
    print(f"📁 输出目录: {base_dir}")
    print("\n⚠️ 提示：音频文件未生成。如需语音播放，运行:")
    print(f"   python generate_audio.py")


if __name__ == "__main__":
    generate_all()
