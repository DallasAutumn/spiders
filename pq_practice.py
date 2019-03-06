from pyquery import PyQuery as pq

html = '''
<!DOCTYPE HTML>
<html>

<head>
    <title>当作业交就好了</title>
    <meta charset="utf-8">
    <style>
        * {
            /*通配符 选择到所有标签*/
            margin: 0;
            padding: 0;
        }

        html {
            height: 100%;
            /*继承父级高度 window*/
        }

        body {
            height: 100%;
            /*继承父级高度 html*/
        }

        ul {
            list-style: none;
            /*清除默认小圆点*/
        }

        .ink-layer {
            width: 100%;
            height: 100%;
            background-image: url();
        }

        .ink-layer:nth-of-type(1) {
            /*css3 子代条件选择器*/
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\藤原妹红（月まで届け、不死の煙）_1386484166572231.jpg)
        }

        .ink-layer:nth-of-type(2) {
            /*css3 子代条件选择器*/
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\八意永琳.png)
        }

        .ink-layer:nth-of-type(3) {
            /*css3 子代条件选择器*/
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\天子.png)
        }

        .ink-layer:nth-of-type(4) {
            /*css3 子代条件选择器*/
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\东方电音精选～速度与节奏碰撞出的激情_3444769938519089.jpg)
        }

        .content {
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            margin: auto;
            width: 1090px;
            height: 429px;
            box-shadow: 0 0 9px #000;
            /*x位移 y位移 羽化半径 颜色*/
        }

        .content ul li {
            float: left;
            /*把元素层级分开，进行浮动*/
            width: 100px;
            height: 429px;
            background-image: url();
        }

        .content ul li:nth-of-type(1) {
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\【万神之纪】取星辰之辉来耀四方_18542164092657303.jpg);
        }

        .content ul li:nth-of-type(2) {
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\【东方Project】一听难忘，永爱东方_1386484173662137.jpg);
        }

        .content ul li:nth-of-type(3) {
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\01e11c58a16ddba801219c7792cf1e.gif);
        }

        .content ul li:nth-of-type(4) {
            width: 789px;
            background-image: url(E:\\学习搞事情\\我爱学习\\跟毓玮哥学coding\\html工作区\\test\\images\\41230366_p0.jpg);
        }

        .content ul li .title {
            width: 100px;
            height: 429px;
            background-color: rgba(0, 0, 0, .5);
        }

        .title p {
            padding: 42px;
            color: #fff;
            font-size: 16px;
        }
    </style>
</head>

<body>
    <div class="ink-layer"></div>
    <div class="ink-layer"></div>
    <div class="ink-layer"></div>
    <div class="ink-layer"></div>
    <div class="content">
        <ul>
            <li>
                <div class="title">
                    <p>i am dqy</p>
                </div>
            </li>
            <li>
                <div class="title">
                    <p>i am dqy</p>
                </div>
            </li>
            <li>
                <div class="title">
                    <p>i am dqy</p>
                </div>
            </li>
            <li style="width:789px;">
                <div class="title">
                    <p>i am dqy</p>
                </div>
            </li>
        </ul>
    </div>
    <script src="E:\学习搞事情\我爱学习\跟毓玮哥学coding\html工作区\test\js\jquery-3.3.1.js"></script>
    <script type="text/javascript">
        $(".content ul li").hover(function(){
            $(this).stop().animate({
                width:"789px"
            },500).siblings().stop().animate({
                width:"100px"
            },500);
        });
    </script>
</body>

</html>
'''

doc = pq(html)

print(doc('li:nth-child(2n-1)'))
