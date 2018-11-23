## 1. Set up and Run the Demo

#### Install CRF++

If Mac, install crf++ at first.

By:

```Shell
$ brew install crf++ 
```

If Window, the crf++ package is included in this project. Don't need to install it.

#### Train a Model

```shell
# generate a model 1a-v50
$ python train.py -m 1a -v vect-50

# generate a model 1abdp
$ python train.py -m 1abdp

# generate a model 2abp
$ python train.py -m 2abp
```



####  Tag a Text File with a Model

```Shell
$ python tagger.py -m 1a-v50 -i demo/input.txt -o demo/output.txt

Loading Model...
Text Input:
--------------------------
今日查房，患者精神、饮食、睡眠可，二便正常，自诉右膝内侧疼痛减轻、活动轻度受限，查体：一般情况可，心肺腹查体未见异常。右膝内侧、右小腿、右踝轻度肿胀略消退，压痛阳性。右膝关节稳定性可。患者要求出院，办理出院。
--------------------------

Entity Result:

+----+------------+-----------+---------+----------+
|    | E-Name     | E-Start   | E-End   | E-Type   |
|----+------------+-----------+---------+----------|
| 0  | 二便       | 17        | 18      | Bo       |
| 1  | 右膝内侧   | 24        | 27      | Bo       |
| 2  | 疼痛       | 28        | 29      | Sy       |
| 3  | 查体       | 40        | 41      | Ch       |
| 4  | 心肺腹查体 | 49        | 53      | Ch       |
| 5  | 右膝       | 59        | 60      | Bo       |
| 6  | 右小腿     | 64        | 66      | Bo       |
| 7  | 右踝       | 68        | 69      | Bo       |
| 8  | 压痛       | 78        | 79      | Ch       |
| 9  | 右膝关节   | 83        | 86      | Bo       |
+----+------------+-----------+---------+----------+

Time Consumption 0.021360 s

```



## 2. Workflows of this Project

## 3. Data Processing

## 4. Understand CRF Model

## 5. Usage of CRF++

## 6. Train Models with Configuration

## 7. Tag Texts with Learned Model 