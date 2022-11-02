# [지원] Apache Kafka

# 0. Concept

- Kafka 란?
    
    Apache Kafka는 LinkedIn에서 개발/ **"분산 메시징 시스템"** (2011년, 오픈소스화(化))
    
    대용량의 실시간 로그처리에 특화된 아키텍쳐 설계 → 기존 메시징 시스템보다 우수한 TPS
    
- 확장성이 뛰어난 분산 메시지 큐(FIFO : First In First Out)
Q. 어떤 부분이 확장성이 뛰어난데? → Scale Out
- 분산 아키텍쳐 구성, Fault-tolerance한 아키텍처(with zookeeper), 데이터 유실 방지를 위한 구성
Q. Fault-Tolerance ? 
→ 파일 시스템에 메시지를 저장하므로, 데이터의 영속성 보장 → 고가용성!
- AMQP, JMS API를 사용하지 않은 TCP기반 프로토콜 사용
Q. AMQP? JMS API? TCP 기반 프로토콜은 뭐가 좋은데?
- **Pub / Sub 메시징 모델**을 채용
Q. Pub/Sub 모델이 뭔데?
    
    [Pub/Sub 모델](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Pub%20Sub%20%E1%84%86%E1%85%A9%E1%84%83%E1%85%A6%E1%86%AF%207f26ef56f9124d9ebb3e6df4fc4b6d42.md)
    
- 읽기/쓰기 성능을 중시
- Producer가 Batch형태로 broker로 메시지 전송이 가능하여 속도 개선
→ Batch 형태로 전송하는 부분이 왜 속도가 개선되지? 속도가 어떻게 개선되는지 궁금해!
- Consume된 메시지를 바로 삭제하지 않고, offset을 통한 consumer-group별 개별 consume가능
→ Consume 된 메시지?
→ Offset ?
→ 개별 Consume?

**# Kafka website url** : [http://kafka.apache.org/](http://kafka.apache.org/)

**# Github url** : [https://github.com/apache/kafka](https://github.com/apache/kafka)

**# Kafka contributors** : [https://github.com/apache/kafka/graphs/contributors](https://github.com/apache/kafka/graphs/contributors)

# Kafka란?

### **_Kafka의 구성 요소 및 동작**

![https://blog.kakaocdn.net/dn/d2nDtD/btqE4pzsyPZ/Tcw9I6z3d7eHjeQ7uaTqa0/img.png](https://blog.kakaocdn.net/dn/d2nDtD/btqE4pzsyPZ/Tcw9I6z3d7eHjeQ7uaTqa0/img.png)

kafka의 기본 구성

- publish-subscribe 모델을 기반으로 동작하며 크게 producer, consumer, broker로 구성
- pub-sub 모델은 메시지를 특정 수신자에게 직접적으로 보내주는 시스템이 아님
- publisher는 메시지를 topic을 통해서 카테고리화
- 분류된 메세지를 받기 위해 subscriber는 그 해당 topic을 subscribe함으로써 메세지를 읽어올 수 있음
- 즉, **publisher, subscriber 모두 topic에 대한 정보만 알고 있음** (publisher/subscriber는 서로 모르는 상태)
- Kafka는 확장성(scale-out)과 고가용성(high availability)을 위하여 broker들이 클러스터로 구성되어 동작하도록 설계
    - 심지어 broker가 1개 밖에 없을 때에도 클러스터로 동작
- 클러스터 내의 broker에 대한 분산처리는 ZooKeeper가 담당

**topic/partition**

- 메시지는 topic으로 분류되고, topic은 여러개의 partition으로 나뉘어진다.
- partition 내의 한 칸은 log라고 불린다.
- 하나의 topic에 여러 개의 partition을 나눠서 메시지를 쓰는 이유? 병렬로 처리하기 위하여 분산 저장을 한다.
    - 한 번 늘린 partition은 줄일 수 없으므로 충분히 고려하여 늘려야함
    - partition을 늘렸을 때, 메시지는 Round-Robin 방식으로 쓰여짐

**broker/zookeeper**

- broker는 kafka의 서버를 말함
- zookeeper는 문산 메세지 큐의 정보를 관리하는 역할 (반드시 필요)

# 1. Kafka  배경

![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled.png)

![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled%201.png)

# 2. terminology

- **Kafka**: 아파치 프로젝트 애플리케이션 이름. kafka cluster 라고도 부름
- **Broker**: 카프카 애플리케이션이 설치되어 있는 서버 혹은 노드
Kafka를 구성하는 각 서버 1대 = 1 broker
- **Topic**: producer 와 consumer 들이 보낸 자신들의 메세지(Data)를 구분하기 위한 네임. 
topic 이라는 개념을 통해 다수의 producer 와 consumer 들이 보낸 메세지를 구분
- **Partition**: 병렬처리가 가능하게 메세지를 나눈 단위
→ 많은 양의 메세지 처리를 위해서는 partition 증가
→ topic이 복사(replicated)되어 나뉘어지는 단위
- **Produdcer & Consumer**: 메세지를 생산하여 broker의 topic으로 보내는 서버 또는 애플리케이션 
& broker 의 topic 으로 저장된 메세지를 가져오는 서버 또는 애플리케이션
    
    **Producer** : Broker에 data를 write하는 역할
    
    **Consumer** : Broker에서 data를 read하는 역할
    
    **Consumer-Group** : 메세지 소비자 묶음 단위(n consumers)
    
- **Zookeeper** : Kafka를 운용하기 위한 Coordination service([zookeeper 소개](http://bcho.tistory.com/1016))

# 3. **Kafka Architecture**

[https://t1.daumcdn.net/cfile/tistory/99B7A03C5C20888D04](https://t1.daumcdn.net/cfile/tistory/99B7A03C5C20888D04)

# 4. Kafka 방식

## 4.1 Pub(Publish) - **Kafka 데이터 쓰기, 복제, 저장**

[https://t1.daumcdn.net/cfile/tistory/996BD43F5C2089EA1C](https://t1.daumcdn.net/cfile/tistory/996BD43F5C2089EA1C)

- 브로커 별로 파티션 나뉘어진 그림

Producer는 1개이상의 partition에 나뉘어 데이터를 write한다.

상기 partition에 적힌 번호는 각 partition의 offset번호임.

각 Topic의 partition은 1개의 Leader Replica + 0개 이상의 follower Replica로 구성

→ Leader Replica에 데이터를 write, 다른 broker에 follower replica로 복제

→ Topic의 데이터(log) 중 replica 데이터는 log segment라는 파일(disk)에 기록

→ 메모리가 남아 있으면 페이지 캐시 사용

## 4.2 Sub(Subscribe) - **Kafka 데이터 읽기**

[https://t1.daumcdn.net/cfile/tistory/99D8AB4F5C208B1B28](https://t1.daumcdn.net/cfile/tistory/99D8AB4F5C208B1B28)

Consumer는 Partition단위로 데이터를 병렬로 읽을 수 있음

→ 복수의 Consumer로 이루어진 Consumer group을 구성하여 1 topic의 데이터를 분산하여 처리 가능

→ **Topic partition number >= Consumer Group number** 일 경우만 가능

(Topic partition number < Consumer Group number일 경우 1개 이상의 consumer는 유휴 상태가 됨)

# 5. K**afka 특징**

[Kafka 특징](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Kafka%20%E1%84%90%E1%85%B3%E1%86%A8%E1%84%8C%E1%85%B5%E1%86%BC%20eb2de6c372b049ea94deafd681dcfc31.md)

[카프카 특징2](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/%E1%84%8F%E1%85%A1%E1%84%91%E1%85%B3%E1%84%8F%E1%85%A1%20%E1%84%90%E1%85%B3%E1%86%A8%E1%84%8C%E1%85%B5%E1%86%BC2%20abc05068e58142469783606186a0a3fb.md)

# 6. **Kafka 사용 주요 사례**

**LinkedIn** : activity streams, operational metrics, data bus(400 nodes, 18k topics, 220B msg/day in May 2014)

**Netflix** : real-time monitoring and event processing

**Twitter** : as part of their Storm real-time data pipelines

**Spotify** : log delivery, Hadoop

**11번가** : 카프카를 이용한 비동기 주문시스템([카프카 컨슈머 애플리케이션 배포 전략 medium post](https://medium.com/11st-pe-techblog/%EC%B9%B4%ED%94%84%EC%B9%B4-%EC%BB%A8%EC%8A%88%EB%A8%B8-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%B0%B0%ED%8F%AC-%EC%A0%84%EB%9E%B5-4cb2c7550a72))

# 7. 메시지 큐 (Kafka vs RabbitMQ 비교)

[메시지 큐](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/%E1%84%86%E1%85%A6%E1%84%89%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8F%E1%85%B2%20b693695c8b2540e18ab4a92645885e89.md)

### **_Kafka의 차별점/장점**

- 기존 메시징 시스템과는 달리 메시지를 파일 시스템에 저장함으로 영속성(durability)이 보장
- consumer가 broker로 부터 직접 메시지를 가지고 가는 pull 방식으로 동작
- **producer 중심적**, 많은 양의 데이터를 파티셔닝하는데에 기반을 둔다
- consumer가 전달 상태를 기억함
- **어마어마한 양의 데이터를 처리**해야 할 때 사용

- kafka가 적절한 곳

Kafka는 복잡한 라우팅에 의존하지 않고 최대 처리량으로 스트리밍하는 데 가장 적합
또한 이벤트 소싱, 스트림 처리 및 일련의 이벤트로 시스템에 대한 모델링 변경을 수행하기 이상적 
Kafka는 다단계 파이프라인에서 데이터를 처리하는 데도 적합
→ 결론적으로 스트리밍 데이터를 저장, 읽기, 다시 읽기 및 분석하는 프레임워크가 필요한 경우
     정기적으로 감사하는 시스템이나 메시지를 영구적으로 저장하는 데 이상적("실시간 처리")

---

[Rabbit MQ](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Rabbit%20MQ%204eb7f6ff0ec540688f05c0edf8198f38.md)

### RabbitMQ vs Kafka

- **RabbitMQ**

![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled%202.png)

- Kafka
    
    ![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled%203.png)
    

- 설계 차이 : RabbitMQ는 메시지 브로커 방식,  Kafka는 pub/sub 방식

   → 메시지 브로커란?
       응용프로그램, 서비스 및 시스템이 정보를 통신하고 교환할 수 있도록 하는 소프트웨어 모듈
       메시지 브로커는 지정된 수신인에게 메시지를 확인, 라우팅, 저장 및 배달       
       브로커는 다른 응용 프로그램 간의 중개자로 작동하여 보낸 사람이 소비자의 위치, 활성 여부, 
       또는 그 중 몇 개가 있는지도 모르게 메시지를 보낼 수 있음

그러나 pub/sub은 생산자가 원하는 각 메시지를 게시할 수 있도록 하는 메시지 배포 패턴

- Kafka는 고성능을 추구하기 때문에 비교적 무거운 편,
따라서 굳이 대용량 데이터를 다루지 않는다면 가벼운 RabbitMQ가 더 나을 수 있음
스트리밍 데이터를 더 쉽게 처리하는 클라이언트 라이브러리 구현인 Kafka Streams도 유용

→ 즉, 사용 목적에 따라서 메시지 큐 방식을 선택해야겠습니다.

- kafka가 적절한 곳

Kafka는 복잡한 라우팅에 의존하지 않고 최대 처리량으로 스트리밍하는 데 가장 적합
또한 이벤트 소싱, 스트림 처리 및 일련의 이벤트로 시스템에 대한 모델링 변경을 수행하기 이상적 
Kafka는 다단계 파이프라인에서 데이터를 처리하는 데도 적합
→ 결론적으로 스트리밍 데이터를 저장, 읽기, 다시 읽기 및 분석하는 프레임워크가 필요한 경우
     정기적으로 감사하는 시스템이나 메시지를 영구적으로 저장하는 데 이상적("실시간 처리")

- RabbitMQ가 적절한 곳

복잡한 라우팅의 경우에는 RabbitMQ를 사용
RabbitMQ는 신속한 요청 - 응답이 필요한 웹 서버에 적합
또한 부하가 높은 작업자(20K 이상 메시지/초) 간에 부하를 공유
백그라운드 작업이나 PDF 변환, 파일 검색 또는 이미지 확장과 같은 장기 실행 작업도 처리 가능

→ 장시간의 Task, 안정적인 백그라운드 작업 실행, 애플리케이션 간 내부 통신/통합이 필요할때

# 0. Concept

- Kafka 란?
    
    Apache Kafka는 LinkedIn에서 개발/ **"분산 메시징 시스템"** (2011년, 오픈소스화(化))
    
    대용량의 실시간 로그처리에 특화된 아키텍쳐 설계 → 기존 메시징 시스템보다 우수한 TPS
    
- 확장성이 뛰어난 분산 메시지 큐(FIFO : First In First Out)
Q. 어떤 부분이 확장성이 뛰어난데? → Scale Out
- 분산 아키텍쳐 구성, Fault-tolerance한 아키텍처(with zookeeper), 데이터 유실 방지를 위한 구성
Q. Fault-Tolerance ? 
→ 파일 시스템에 메시지를 저장하므로, 데이터의 영속성 보장 → 고가용성!
- AMQP, JMS API를 사용하지 않은 TCP기반 프로토콜 사용
Q. AMQP? JMS API? TCP 기반 프로토콜은 뭐가 좋은데?
- **Pub / Sub 메시징 모델**을 채용
Q. Pub/Sub 모델이 뭔데?
    
    [Pub/Sub 모델](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Pub%20Sub%20%E1%84%86%E1%85%A9%E1%84%83%E1%85%A6%E1%86%AF%208ff8112b3af04fe186a0772e6e3538d4.md)
    
- 읽기/쓰기 성능을 중시
- Producer가 Batch형태로 broker로 메시지 전송이 가능하여 속도 개선
→ Batch 형태로 전송하는 부분이 왜 속도가 개선되지? 속도가 어떻게 개선되는지 궁금해!
- Consume된 메시지를 바로 삭제하지 않고, offset을 통한 consumer-group별 개별 consume가능
→ Consume 된 메시지?
→ Offset ?
→ 개별 Consume?

**# Kafka website url** : [http://kafka.apache.org/](http://kafka.apache.org/)

**# Github url** : [https://github.com/apache/kafka](https://github.com/apache/kafka)

**# Kafka contributors** : [https://github.com/apache/kafka/graphs/contributors](https://github.com/apache/kafka/graphs/contributors)

# Kafka란?

### **_Kafka의 구성 요소 및 동작**

![https://blog.kakaocdn.net/dn/d2nDtD/btqE4pzsyPZ/Tcw9I6z3d7eHjeQ7uaTqa0/img.png](https://blog.kakaocdn.net/dn/d2nDtD/btqE4pzsyPZ/Tcw9I6z3d7eHjeQ7uaTqa0/img.png)

kafka의 기본 구성

- publish-subscribe 모델을 기반으로 동작하며 크게 producer, consumer, broker로 구성
- pub-sub 모델은 메시지를 특정 수신자에게 직접적으로 보내주는 시스템이 아님
- publisher는 메시지를 topic을 통해서 카테고리화
- 분류된 메세지를 받기 위해 subscriber는 그 해당 topic을 subscribe함으로써 메세지를 읽어올 수 있음
- 즉, **publisher, subscriber 모두 topic에 대한 정보만 알고 있음** (publisher/subscriber는 서로 모르는 상태)
- Kafka는 확장성(scale-out)과 고가용성(high availability)을 위하여 broker들이 클러스터로 구성되어 동작하도록 설계
    - 심지어 broker가 1개 밖에 없을 때에도 클러스터로 동작
- 클러스터 내의 broker에 대한 분산처리는 ZooKeeper가 담당

**topic/partition**

- 메시지는 topic으로 분류되고, topic은 여러개의 partition으로 나뉘어진다.
- partition 내의 한 칸은 log라고 불린다.
- 하나의 topic에 여러 개의 partition을 나눠서 메시지를 쓰는 이유? 병렬로 처리하기 위하여 분산 저장을 한다.
    - 한 번 늘린 partition은 줄일 수 없으므로 충분히 고려하여 늘려야함
    - partition을 늘렸을 때, 메시지는 Round-Robin 방식으로 쓰여짐

**broker/zookeeper**

- broker는 kafka의 서버를 말함
- zookeeper는 문산 메세지 큐의 정보를 관리하는 역할 (반드시 필요)

# 1. Kafka  배경

![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled.png)

![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled%201.png)

# 2. terminology

- **Kafka**: 아파치 프로젝트 애플리케이션 이름. kafka cluster 라고도 부름
- **Broker**: 카프카 애플리케이션이 설치되어 있는 서버 혹은 노드
Kafka를 구성하는 각 서버 1대 = 1 broker
- **Topic**: producer 와 consumer 들이 보낸 자신들의 메세지(Data)를 구분하기 위한 네임. 
topic 이라는 개념을 통해 다수의 producer 와 consumer 들이 보낸 메세지를 구분
- **Partition**: 병렬처리가 가능하게 메세지를 나눈 단위
→ 많은 양의 메세지 처리를 위해서는 partition 증가
→ topic이 복사(replicated)되어 나뉘어지는 단위
- **Produdcer & Consumer**: 메세지를 생산하여 broker의 topic으로 보내는 서버 또는 애플리케이션 
& broker 의 topic 으로 저장된 메세지를 가져오는 서버 또는 애플리케이션
    
    **Producer** : Broker에 data를 write하는 역할
    
    **Consumer** : Broker에서 data를 read하는 역할
    
    **Consumer-Group** : 메세지 소비자 묶음 단위(n consumers)
    
- **Zookeeper** : Kafka를 운용하기 위한 Coordination service([zookeeper 소개](http://bcho.tistory.com/1016))

# 3. **Kafka Architecture**

[https://t1.daumcdn.net/cfile/tistory/99B7A03C5C20888D04](https://t1.daumcdn.net/cfile/tistory/99B7A03C5C20888D04)

# 4. Kafka 방식

## 4.1 Pub(Publish) - **Kafka 데이터 쓰기, 복제, 저장**

[https://t1.daumcdn.net/cfile/tistory/996BD43F5C2089EA1C](https://t1.daumcdn.net/cfile/tistory/996BD43F5C2089EA1C)

- 브로커 별로 파티션 나뉘어진 그림

Producer는 1개이상의 partition에 나뉘어 데이터를 write한다.

상기 partition에 적힌 번호는 각 partition의 offset번호임.

각 Topic의 partition은 1개의 Leader Replica + 0개 이상의 follower Replica로 구성

→ Leader Replica에 데이터를 write, 다른 broker에 follower replica로 복제

→ Topic의 데이터(log) 중 replica 데이터는 log segment라는 파일(disk)에 기록

→ 메모리가 남아 있으면 페이지 캐시 사용

## 4.2 Sub(Subscribe) - **Kafka 데이터 읽기**

[https://t1.daumcdn.net/cfile/tistory/99D8AB4F5C208B1B28](https://t1.daumcdn.net/cfile/tistory/99D8AB4F5C208B1B28)

Consumer는 Partition단위로 데이터를 병렬로 읽을 수 있음

→ 복수의 Consumer로 이루어진 Consumer group을 구성하여 1 topic의 데이터를 분산하여 처리 가능

→ **Topic partition number >= Consumer Group number** 일 경우만 가능

(Topic partition number < Consumer Group number일 경우 1개 이상의 consumer는 유휴 상태가 됨)

# 5. K**afka 특징**

[Kafka 특징 (1)](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Kafka%20%E1%84%90%E1%85%B3%E1%86%A8%E1%84%8C%E1%85%B5%E1%86%BC%20(1)%20c232e7d8c1294de0b92e359811d9789a.md)

[카프카 특징2 (1)](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/%E1%84%8F%E1%85%A1%E1%84%91%E1%85%B3%E1%84%8F%E1%85%A1%20%E1%84%90%E1%85%B3%E1%86%A8%E1%84%8C%E1%85%B5%E1%86%BC2%20(1)%20ec10ffa658cb4515ac51214a4797e45c.md)

# 6. **Kafka 사용 주요 사례**

**LinkedIn** : activity streams, operational metrics, data bus(400 nodes, 18k topics, 220B msg/day in May 2014)

**Netflix** : real-time monitoring and event processing

**Twitter** : as part of their Storm real-time data pipelines

**Spotify** : log delivery, Hadoop

**11번가** : 카프카를 이용한 비동기 주문시스템([카프카 컨슈머 애플리케이션 배포 전략 medium post](https://medium.com/11st-pe-techblog/%EC%B9%B4%ED%94%84%EC%B9%B4-%EC%BB%A8%EC%8A%88%EB%A8%B8-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%B0%B0%ED%8F%AC-%EC%A0%84%EB%9E%B5-4cb2c7550a72))

# 7. 메시지 큐 (Kafka vs RabbitMQ 비교)

[메시지 큐 (1)](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/%E1%84%86%E1%85%A6%E1%84%89%E1%85%B5%E1%84%8C%E1%85%B5%20%E1%84%8F%E1%85%B2%20(1)%20bdee9a8da12a4635b3cd2fc90f1f7bae.md)

### **_Kafka의 차별점/장점**

- 기존 메시징 시스템과는 달리 메시지를 파일 시스템에 저장함으로 영속성(durability)이 보장
- consumer가 broker로 부터 직접 메시지를 가지고 가는 pull 방식으로 동작
- **producer 중심적**, 많은 양의 데이터를 파티셔닝하는데에 기반을 둔다
- consumer가 전달 상태를 기억함
- **어마어마한 양의 데이터를 처리**해야 할 때 사용

- kafka가 적절한 곳

Kafka는 복잡한 라우팅에 의존하지 않고 최대 처리량으로 스트리밍하는 데 가장 적합
또한 이벤트 소싱, 스트림 처리 및 일련의 이벤트로 시스템에 대한 모델링 변경을 수행하기 이상적 
Kafka는 다단계 파이프라인에서 데이터를 처리하는 데도 적합
→ 결론적으로 스트리밍 데이터를 저장, 읽기, 다시 읽기 및 분석하는 프레임워크가 필요한 경우
     정기적으로 감사하는 시스템이나 메시지를 영구적으로 저장하는 데 이상적("실시간 처리")

---

[Rabbit MQ (1)](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Rabbit%20MQ%20(1)%202f4fb7ae038149fbaef0ece19535c33d.md)

### RabbitMQ vs Kafka

- **RabbitMQ**

![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled%202.png)

- Kafka
    
    ![Untitled](%5B%E1%84%8C%E1%85%B5%E1%84%8B%E1%85%AF%E1%86%AB%5D%20Apache%20Kafka%20d8fdb6cc00334ae0a7a2e0f9c76b1237/Untitled%203.png)
    

- 설계 차이 : RabbitMQ는 메시지 브로커 방식,  Kafka는 pub/sub 방식

   → 메시지 브로커란?
       응용프로그램, 서비스 및 시스템이 정보를 통신하고 교환할 수 있도록 하는 소프트웨어 모듈
       메시지 브로커는 지정된 수신인에게 메시지를 확인, 라우팅, 저장 및 배달       
       브로커는 다른 응용 프로그램 간의 중개자로 작동하여 보낸 사람이 소비자의 위치, 활성 여부, 
       또는 그 중 몇 개가 있는지도 모르게 메시지를 보낼 수 있음

그러나 pub/sub은 생산자가 원하는 각 메시지를 게시할 수 있도록 하는 메시지 배포 패턴

- Kafka는 고성능을 추구하기 때문에 비교적 무거운 편,
따라서 굳이 대용량 데이터를 다루지 않는다면 가벼운 RabbitMQ가 더 나을 수 있음
스트리밍 데이터를 더 쉽게 처리하는 클라이언트 라이브러리 구현인 Kafka Streams도 유용

→ 즉, 사용 목적에 따라서 메시지 큐 방식을 선택해야겠습니다.

- kafka가 적절한 곳

Kafka는 복잡한 라우팅에 의존하지 않고 최대 처리량으로 스트리밍하는 데 가장 적합
또한 이벤트 소싱, 스트림 처리 및 일련의 이벤트로 시스템에 대한 모델링 변경을 수행하기 이상적 
Kafka는 다단계 파이프라인에서 데이터를 처리하는 데도 적합
→ 결론적으로 스트리밍 데이터를 저장, 읽기, 다시 읽기 및 분석하는 프레임워크가 필요한 경우
     정기적으로 감사하는 시스템이나 메시지를 영구적으로 저장하는 데 이상적("실시간 처리")

- RabbitMQ가 적절한 곳

복잡한 라우팅의 경우에는 RabbitMQ를 사용
RabbitMQ는 신속한 요청 - 응답이 필요한 웹 서버에 적합
또한 부하가 높은 작업자(20K 이상 메시지/초) 간에 부하를 공유
백그라운드 작업이나 PDF 변환, 파일 검색 또는 이미지 확장과 같은 장기 실행 작업도 처리 가능

→ 장시간의 Task, 안정적인 백그라운드 작업 실행, 애플리케이션 간 내부 통신/통합이 필요할때
