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



####  Tagger a Text File with a Model

```shell
$ python tagger.py -m 1a-v50 -i demo/input.txt -o demo/output.txt
```



## 2. Workflows of this Project

## 3. Data Processing

## 4. Understand CRF Model

## 5. Usage of CRF++

## 6. Train Models with Configuration

## 7. Tag Texts with Learned Model 