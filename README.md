

# PaKoML Toilet Paper Recognition Project

<p align = "center">
<img src = "https://user-images.githubusercontent.com/19871043/177982170-974040ea-9c6a-4a7c-ad6a-3b2947577a38.png" width="150px" height="150px">
</p>

<div align = "center"> 
  
![license](https://img.shields.io/github/license/PaKoML/Toilet_Paper_Recognition.svg)
![repo size in bytes](https://img.shields.io/github/repo-size/PaKoML/Toilet_Paper_Recognition.svg)
![GitHub contributors](https://img.shields.io/github/contributors/PaKoML/Toilet_Paper_Recognition.svg)
![GitHub commit](https://img.shields.io/github/last-commit/PaKoML/Toilet_Paper_Recognition.svg)
![GitHub commit interval](https://img.shields.io/github/commit-activity/w/PaKoML/Toilet_Paper_Recognition.svg)
</div>

## Introduction
<p>
We are sometimes very confused with which orientation is appropriate for a roll of tissue when it is hung on a hanger. The initial patent of the toilet-roll dispenser<a href = "#tag_one">[1]</a> and Covid-19 recommendations advise to hang tissues in over direction, while opposition has been raised that hanging in the under direction can prevent the ruin of unrolling all toilet papers from cats, toddlers, and vibration.<a href = "#tag_two">[2]</a>

Whoever supports either side, changing all the tissues in the world to the direction they support has become a practical dogma. However, 42 million tons of toilet papers are consumed every year<a href = "#tag_three">[3]</a>, and the whole usage of tissues is expected to increase steadily in the future.<a href = "#tag_four">[4]</a> Therefore, it is expected that astronomical costs will be spent on searching for and modifying all the toilet paper rolls. Even if a place where they are likely to be hung is monitored using CCTV, it is obvious that a bottleneck occurs if manpower is involved in the toilet paper recognition process.

Therefore, judging where and how toilet papers are hung within a given image has become a global challenge. The PaKoML Toilet Paper Recognition Machine transform this recognition into a full-automatic process and opens a new horizon for the discourse of toilet paper orientation.
</p>

<details>
    <summary>korean version introduction</summary>
    <p><br>&nbsp;&nbsp;우리가 때때로 대단히 혼란스럽게 느끼는 것은, 두루마리 휴지가 휴지걸이에 걸려있을 때 어느 방향으로 풀려있는 것이 적절한가 하는 점이다. 휴지걸이의 초기 특허와 관련된 증거들과<a href = "#tag_one">[1]</a> covid-19 권고사항들은 over 방향을 권고하는 경우가 있는가 하면, under 방향으로 걸어놓은 경우 고양이와 어린 아이들, 진동으로부터 휴지가 몽땅 풀리는 참상을 막을 수 있다는 반대 의견이 제기된 바 있다.<a href = "#tag_two">[2]</a>
      
  &nbsp;&nbsp;어느 쪽을 지지하는 사람이건, 세상에 걸려있는 모든 휴지를 자신이 지지하는 방향으로 바꾸어 걸어놓는 것은 하나의 실천적 도그마가 되었다. 하지만 매 해 4200만 톤의 휴지가 사용되고<a href = "#tag_three">[3]</a> 앞으로도 휴지 사용량이 꾸준히 증가할 것으로 예상되는 실정이다.<a href = "#tag_four">[4]</a> 따라서 휴지가 걸려있는 모든 장소를 찾아다니며 그를 수정하는 것은 천문학적인 사회적 비용이 소모될 것으로 예측된다. CCTV를 이용하여 휴지가 걸려있을 법한 장소를 모니터링하더라도, 인력이 휴지 인식 과정(toilet paper recognition process)에 수반되는 순간 병목 현상이 유발됨은 자명하다.
      
  &nbsp;&nbsp;따라서 주어진 이미지 안에서 휴지가 어디에 어떻게 걸려있는가를 판단하는 것은 전인류적 숙제가 되었다. PaKoML Toilet Paper Recognition Machine은 이러한 인식 과정을 완전한 자동화 과정으로 탈피시키고, 두루마리 휴지 방향(toilet paper direction) 담론에 새로운 지평을 연다.</p>
</details>

## How To Use

The preview model is available <a href = "https://jordano112.run.goorm.io/">here</a>.
<h4>1. Click "choose image"<h4>
<p align = "center">
<img width="949" alt="IMG_0234" src="https://user-images.githubusercontent.com/62343298/178098915-5941ba94-750d-4ce2-be48-423b45a02976.PNG">
</p>
  
<h4>2. Select a picture and click "Open"<h4>
<p align = "center">
<img width="959" alt="IMG_0235" src="https://user-images.githubusercontent.com/62343298/178098916-dd2b3556-52ea-4483-bb4a-9cbf921e28e0.PNG">
</p>
    
<h4>3. Click "Submit"<h4>
<p align = "center">
<img width="953" alt="IMG_0236" src="https://user-images.githubusercontent.com/62343298/178098917-d93fbb13-40b0-4985-b227-bacd0941f655.PNG">  
</p>

<h4>4. Check the result<h4>
<p align = "center">
<img width="951" alt="화면 캡처 2022-07-09 164915" src="https://user-images.githubusercontent.com/62343298/178099011-da8837eb-1fed-4b9f-b5f6-bf233c38b6ae.png">
  </p>
  
## Model overview
VGGNet(VGG16)<a href = "#tag_four">[5]</a> is used for feature extraction from image, then feature vector is computed in two submodel : category classifier and bounding box regressor. 

<p align = "center">
<img src = "https://user-images.githubusercontent.com/19871043/177984627-b1ef4c78-915b-4abf-9212-3a58348ee8b7.png" width="500px">
</p>
(image from https://neurohive.io/en/popular-networks/vgg16/)
<br><br>
Instead of using full VGG16 model, we changed fully-connected layer part to two predictor. The details are shown in below.

<p align = "center">
<img src = "https://user-images.githubusercontent.com/19871043/178096409-dbd26b40-aba0-416d-b690-247f8a222388.png" width="500px">
</p>

### Datasets
We trained our model on 580 images of toilet paper dispensor picture annotated with a bounding box manually drawn by us. The data is consists of 264 over pictures, 195 vertical or unspecified pictures, and 41 under pictures. To draw bounding box and load data, <a href = "https://app.labelbox.com/">labelbox</a> is used.

### Details of our learning
We trained our model using Adams with learning rate = 3e-5, batch size = 5, no learning decay scheduling, and 40 Epochs. For loss function, MSELoss is used and the loses from bounding box regressor and category classifier is added after multipling 10 to the loss of category classifier to get a balance between them.

You can see loss log below, and accuarcy is not noted because we validated our learning by just watching how our model draws bounding box and predicts class on unseen data. 

![image](https://user-images.githubusercontent.com/19871043/178096753-dbf8092d-546c-43fa-ab0a-ddbb47605307.png)





### References
<div id = "tag_one"></div>
[1] Mitchell, Kathy; Sugar, Marcy (19 April 2005a), "Annie's Mailbox: Friend's abuse should be reported" (PDF), Vernon Daily Record, p. 6, retrieved 3 July 2010[permanent dead link]
<br><br>
<div id = "tag_two"></div>
[2] Nerbas, Reena (4 October 2009), "Pesky glue: Peanut butter to the rescue", Winnipeg Free Press, p. D2, Factiva WFP0000020091004e5a40000h
<br><br>
<div id = "tag_three"></div>
[3] Statistica. (n.d.). Retrieved July 1, 2022, from https://www.statista.com/outlook/cmo/tissue-hygiene-paper/toilet-paper/worldwide
<br><br>
<div id = "tag_four"></div>
[4] Fortune Business Insights. (n.d.). Retrieved July 1, 2022, from https://www.fortunebusinessinsights.com/toilet-paper-market-104298
<br><br>
<div id = "tag_five"></div>
[5] Simonyan, K., & Zisserman, A. (2014). Very deep convolutional networks for large-scale image recognition. arXiv preprint arXiv:1409.1556.



## Developers
* [Minjun Kim](https://github.com/kmj0825) 
* [Hanbin Park](https://github.com/kimchyoungman)
* [Jihwan Hong](https://github.com/Jordano-Jackson)
