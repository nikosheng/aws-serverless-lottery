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

## 参考

