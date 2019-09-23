# aws-serverless-lottery
在本次实验中，我们将会通过AWS Serverless应用构建一个无服务器化的抽奖程序。本次的实验涉及到的服务有：
- [AWS Lambda](https://aws.amazon.com/lambda/)
- [Amazon API Gateway](https://aws.amazon.com/api-gateway/)
- [AWS Step Functions](https://aws.amazon.com/step-functions/)
- [Amazon SNS](https://aws.amazon.com/sns/)
- [Amazon Dynamodb](https://aws.amazon.com/dynamodb/)


## 前提条件
- 本文实验基于AWS中国区宁夏区(cn-northwest-1)作示例。所有控制台链接均直接连接到北京区console。如使用海外区账号，请不要点击此直达连接，在global控制台选择相应产品即可。
- 如果您使用的是AWS中国区账号，账号默认屏蔽了80,8080,443三个端口，需要先申请打开443端口才可以正常使用API Gateway的服务。如果是海外账号，没有此限制。
- 如何判断自己的账号是中国区账号还是海外区账号？请查看自己的控制台链接，console.amazonaws.cn为中国区，console.aws.amazon.com为海外区账号。

## Architecture
![Architecture](docs/img/architecture.png)

## Workflow Overview
![Workflow](docs/img/workflow.png)

## 详细步骤

### 创建AWS Step Functions 状态机

1. 进入AWS控制台，在`服务`中搜索`Step Functions`
2. 进入`Step Functions`服务后，点击左侧的活动栏，并点击`状态机`
3. 进入`状态机`主页面后，选择`创建状态机`
4. 在`定义状态机`栏目下，选择默认`使用代码段创作`。同时在`详细信息`栏目输入状态机名称`Lottery`
5. 在`状态机定义`栏目下，复制如下状态机定义文件，通过`Amazon States Language`来定义状态机的状态流转
```
{
  "Comment": "A simple AWS Step Functions state machine that simulates the lottery session",
  "StartAt": "Input Lottery Winners",
  "States": {
    "Input Lottery Winners": {
        "Type": "Task",
        "Resource": "arn:aws:lambda:ap-southeast-1:379951292773:function:Lottery-InputWinners",
        "ResultPath": "$",
        "Catch": [ 
            {          
              "ErrorEquals": [ "CustomError" ],
              "Next": "Failed"      
            },
            {          
              "ErrorEquals": [ "States.ALL" ],
              "Next": "Failed"      
            } 
          ],
        "Next": "Random Select Winners"
    }, 
    "Random Select Winners": {
      "Type": "Task",
      "InputPath": "$.body",
      "Resource": "arn:aws:lambda:ap-southeast-1:379951292773:function:Lottery-RandomSelectWinners",
      "Catch": [ 
        {          
          "ErrorEquals": [ "States.ALL" ],
          "Next": "Failed"      
        } 
      ],      
     "Retry": [ 
        {
          "ErrorEquals": [ "States.ALL"],          
          "IntervalSeconds": 1, 
          "MaxAttempts": 2
        } 
      ],
      "Next": "Validate Winners"
    },
    "Validate Winners": {
      "Type": "Task",
      "InputPath": "$.body",
      "Resource": "arn:aws:lambda:ap-southeast-1:379951292773:function:Lottery-ValidateWinners",
      "Catch": [ 
        {          
          "ErrorEquals": [ "States.ALL" ],
          "Next": "Failed"      
        } 
      ],      
     "Retry": [ 
        {
          "ErrorEquals": [ "States.ALL"],          
          "IntervalSeconds": 1, 
          "MaxAttempts": 2
        } 
      ],
      "Next": "Is Winner In Past Draw"
    },
    "Is Winner In Past Draw": {
      "Type" : "Choice",
        "Choices": [
          {
            "Variable": "$.status",
            "NumericEquals": 0,
            "Next": "Send SNS and Record In Dynamodb"
          },
          {
            "Variable": "$.status",
            "NumericEquals": 1,
            "Next": "Random Select Winners"
          }
      ]
    },
    "Send SNS and Record In Dynamodb": {
      "Type": "Parallel",
      "End": true,
      "Catch": [ 
        {          
          "ErrorEquals": [ "States.ALL" ],
          "Next": "Failed"      
        } 
      ],      
     "Retry": [ 
        {
          "ErrorEquals": [ "States.ALL"],          
          "IntervalSeconds": 1, 
          "MaxAttempts": 2
        } 
      ],
      "Branches": [
        {
         "StartAt": "Notify Winners",
         "States": {
           "Notify Winners": {
             "Type": "Task",
             "Resource": "arn:aws:states:::sns:publish",
             "Parameters": {
               "TopicArn": "arn:aws:sns:ap-southeast-1:379951292773:Lottery-Notification",
               "Message.$": "$.sns"
             },
             "End": true
           }
         }
       },
       {
         "StartAt": "Record Winner Queue",
         "States": {
           "Record Winner Queue": {
             "Type": "Task",
             "InputPath": "$.body",
             "Resource":
               "arn:aws:lambda:ap-southeast-1:379951292773:function:Lottery-RecordWinners",
             "TimeoutSeconds": 300,
             "End": true
           }
         }
       }
      ]
    },
    "Failed": {
        "Type": "Fail"
     }
  }
}
```
6. 在`状态机定义`栏目的右侧，点击`刷新`按钮，可以看到状态机流转的流程图。点击`下一步`
7. 在`配置设置`下，选择`为我创建IAM角色`, 输入自定义的IAM角色名称`MyStepFunctionsExecutionRole`
8. 点击`创建状态机`完成创建过程

## 参考

