

# PaKoML Toilet Paper Recognition Project

<p align = "center">
<img src = "https://user-images.githubusercontent.com/19871043/177982170-974040ea-9c6a-4a7c-ad6a-3b2947577a38.png" width="150px" height="150px">
</p>

<div align = "center"> 
  
![license](https://img.shields.io/github/license/osamhack2021/PaKoML/Toilet_Paper_Recognition.svg)
![repo size in bytes](https://img.shields.io/github/repo-size/PaKoML/Toilet_Paper_Recognition.svg)
![GitHub contributors](https://img.shields.io/github/contributors/PaKoML/Toilet_Paper_Recognition.svg)
![GitHub commit](https://img.shields.io/github/last-commit/PaKoML/Toilet_Paper_Recognition.svg)
![GitHub commit interval](https://img.shields.io/github/commit-activity/w/PaKoML/Toilet_Paper_Recognition.svg)
</div>

## Introduction
<p>
We are sometimes very confused with which orientation is appropriate for a roll of tissue when it is hung on a hanger. The initial patent of the toilet-roll dispenser[1] and Covid-19 recommendations advise to hang tissues in over direction, while opposition has been raised that hanging in the under direction can prevent the ruin of unrolling all toilet papers from cats, toddlers, and vibration.[2]

Whoever supports either side, changing all the tissues in the world to the direction they support has become a practical dogma. However, 42 million tons of toilet papers are consumed every year[3], and the whole usage of tissues is expected to increase steadily in the future.[4] Therefore, it is expected that astronomical costs will be spent on searching for and modifying all the toilet paper rolls. Even if a place where they are likely to be hung is monitored using CCTV, it is obvious that a bottleneck occurs if manpower is involved in the toilet paper recognition process.

Therefore, judging where and how toilet papers are hung within a given image has become a global challenge. The PaKoML Toilet Paper Recognition Machine transform this recognition into a full-automatic process and opens a new horizon for the discourse of toilet paper orientation.
</p>


## How To Use

The preview model is available <a href = "https://jordano112.run.goorm.io/">here</a>.


## Model overview
VGGNet(VGG16)[5] is used for feature extraction from image, then feature vector is computed in two submodel : category classifier and bounding box regressor. 

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
[1] Mitchell, Kathy; Sugar, Marcy (19 April 2005a), "Annie's Mailbox: Friend's abuse should be reported" (PDF), Vernon Daily Record, p. 6, retrieved 3 July 2010[permanent dead link]

[2] Nerbas, Reena (4 October 2009), "Pesky glue: Peanut butter to the rescue", Winnipeg Free Press, p. D2, Factiva WFP0000020091004e5a40000h

[3] Statistica. (n.d.). Retrieved July 1, 2022, from https://www.statista.com/outlook/cmo/tissue-hygiene-paper/toilet-paper/worldwide

[4] Fortune Business Insights. (n.d.). Retrieved July 1, 2022, from https://www.fortunebusinessinsights.com/toilet-paper-market-104298

[5] Simonyan, K., & Zisserman, A. (2014). Very deep convolutional networks for large-scale image recognition. arXiv preprint arXiv:1409.1556.



## Developers
* [Minjun Kim](https://github.com/kmj0825) 
* [Hanbin Park](https://github.com/kimchyoungman)
* [Jihwan Hong](https://github.com/Jordano-Jackson)
