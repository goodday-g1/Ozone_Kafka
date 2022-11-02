# Apache Kafka Concept

# 0. Concept

- Kafka 란?
  > Apache Kafka는 LinkedIn에서 개발/ **"분산 메시징 시스템"** (2011년, 오픈소스화(化))  
  > 대용량의 실시간 로그처리에 특화된 아키텍쳐 설계 → 기존 메시징 시스템보다 우수한 TPS  
  > 확장성이 뛰어난 분산 메시지 큐(FIFO : First In First Out)
  > **Pub(Publisher)/Sub(Subscriber) 메시징 모델**을 채용
  > 읽기/쓰기 성능을 중시
  > Producer가 Batch형태로 broker로 메시지 전송이 가능하여 속도 개선

- 궁금증 🎈
  - Q. 어떤 부분이 확장성이 뛰어난데? → Scale Out
  > 분산 아키텍쳐 구성, Fault-tolerance한 아키텍처(with zookeeper), 데이터 유실 방지를 위한 구성

  - Q. Fault-Tolerance ? 
  > 파일 시스템에 메시지를 저장하므로, 데이터의 영속성 보장 → 고가용성!
  > AMQP, JMS API를 사용하지 않은 TCP기반 프로토콜 사용
 
  - Q. AMQP? JMS API? 
  > TCP 기반 프로토콜은 뭐가 좋은데?

  - Q. Batch 형태로 전송하는 부분이 왜 속도가 개선되지? 속도가 어떻게 개선되는지 궁금해!
  > Consume된 메시지를 바로 삭제하지 않고, offset을 통한 consumer-group별 개별 consume가능
  > Consume 된 메시지? Offset ? 개별 Consume?  공부할 거 투성이!

<br>

**# Kafka website url** :[http://kafka.apache.org/](http://kafka.apache.org/)    
**# Github url** : [https://github.com/apache/kafka](https://github.com/apache/kafka)    
**# Kafka contributors** : [https://github.com/apache/kafka/graphs/contributors](https://github.com/apache/kafka/graphs/contributors)    

<br>

# 1. Kafka란?

## **_Kafka의 구성 요소 및 동작**

- publish-subscribe 모델을 기반으로 동작하며 크게 producer, consumer, broker로 구성  
  > pub-sub 모델은 메시지를 특정 수신자에게 직접적으로 보내주는 시스템이 아님  
  > publisher는 메시지를 topic을 통해서 카테고리화  
  > 분류된 메세지를 받기 위해 subscriber는 그 해당 topic을 subscribe함으로써 메세지를 읽어올 수 있음  
  > 즉, **publisher, subscriber 모두 topic에 대한 정보만 알고 있음** (publisher/subscriber는 서로 모르는 상태)  
- Kafka는 확장성(scale-out)과 고가용성(high availability)을 위하여 broker들이 클러스터로 구성되어 동작하도록 설계  
  > 심지어 broker가 1개 밖에 없을 때에도 클러스터로 동작  
- 클러스터 내의 broker에 대한 분산처리는 ZooKeeper가 담당  


## **topic/partition**

- 메시지는 topic으로 분류되고, topic은 여러개의 partition으로 나뉘어진다.
- partition 내의 한 칸은 log라고 불린다.
- 하나의 topic에 여러 개의 partition을 나눠서 메시지를 쓰는 이유? 병렬로 처리하기 위하여 분산 저장을 한다.
  > 한 번 늘린 partition은 줄일 수 없으므로 충분히 고려하여 늘려야함
  > partition을 늘렸을 때, 메시지는 Round-Robin 방식으로 쓰여짐


## **broker/zookeeper**

- broker는 kafka의 서버를 말함
- zookeeper는 문산 메세지 큐의 정보를 관리하는 역할 (반드시 필요)


# 2. terminology

- **Kafka**: 아파치 프로젝트 애플리케이션 이름. kafka cluster 라고도 부름   

- **Broker**: 카프카 애플리케이션이 설치되어 있는 서버 혹은 노드  
  > Kafka를 구성하는 각 서버 1대 = 1 broker  

- **Topic**: producer 와 consumer 들이 보낸 자신들의 메세지(Data)를 구분하기 위한 네임.     
  > topic 이라는 개념을 통해 다수의 producer 와 consumer 들이 보낸 메세지를 구분  

- **Partition**: 병렬처리가 가능하게 메세지를 나눈 단위  
  > 많은 양의 메세지 처리를 위해서는 partition 증가  
  > topic이 복사(replicated)되어 나뉘어지는 단위  

- **Produdcer & Consumer**: 메세지를 생산하여 broker의 topic으로 보내는 서버 또는 애플리케이션   
  > broker 의 topic 으로 저장된 메세지를 가져오는 서버 또는 애플리케이션  
    
- **Producer** : Broker에 data를 write하는 역할
    
- **Consumer** : Broker에서 data를 read하는 역할
    
- **Consumer-Group** : 메세지 소비자 묶음 단위(n consumers)
    
- **Zookeeper** : Kafka를 운용하기 위한 Coordination service



# 3. Kafka 사용 주요 사례

- **LinkedIn** : activity streams, operational metrics, data bus(400 nodes, 18k topics, 220B msg/day in May 2014)  
 
- **Netflix** : real-time monitoring and event processing  

- **Twitter** : as part of their Storm real-time data pipelines  

- **Spotify** : log delivery, Hadoop

- **11번가** : 카프카를 이용한 비동기 주문시스템([카프카 컨슈머 애플리케이션 배포 전략 medium post](https://medium.com/11st-pe-techblog/%EC%B9%B4%ED%94%84%EC%B9%B4-%EC%BB%A8%EC%8A%88%EB%A8%B8-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%B0%B0%ED%8F%AC-%EC%A0%84%EB%9E%B5-4cb2c7550a72))

# 4. Kafka의 차별점/장점

- 기존 메시징 시스템과는 달리 메시지를 파일 시스템에 저장함으로 영속성(durability)이 보장  
- consumer가 broker로 부터 직접 메시지를 가지고 가는 pull 방식으로 동작  
- **producer 중심적**, 많은 양의 데이터를 파티셔닝하는데에 기반을 둔다  
- consumer가 전달 상태를 기억함  
- **어마어마한 양의 데이터를 처리**해야 할 때 사용  

# 5. kafka가 적절한 곳

- Kafka는 복잡한 라우팅에 의존하지 않고 최대 처리량으로 스트리밍하는 데 가장 적합  
- 이벤트 소싱, 스트림 처리 및 일련의 이벤트로 시스템에 대한 모델링 변경을 수행하기 이상적   
- Kafka는 다단계 파이프라인에서 데이터를 처리하는 데도 적합  

<br>
- 결론적으로 스트리밍 데이터를 저장, 읽기, 다시 읽기 및 분석하는 프레임워크가 필요한 경우
  > 정기적으로 감사하는 시스템이나 메시지를 영구적으로 저장하는 데 이상적("실시간 처리")
