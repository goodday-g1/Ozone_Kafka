# 참고 강의. Kafka _ Dev원영
- https://www.youtube.com/watch?v=catN_YhV6To
## **Kafka  기본 개념 및 생태계**

### 배경
**As - Is**
- end to end  연결 방식 아키텍처 많이 사용하다 보니, 데이터 연동의 복잡성이 증가
- 각각의 하드웨어/운영체제가 다르다 보니, 너무 많은 운영요소를 고려하게 됨
- 예를 들어, MySQL 에서 하둡으로 데이터를 보내거나 MySQL에서 모니터링을 위한 DB에 보낼 때마다   
  각기 다른 파이프라인 연결 구조가 필요 -> 코드의 복잡성 증가
  
  -> LinkIn에서 위 문제를 해결하기 위해, 모든 시스템으로 데이터 전송이 가능하면서,   
     실시간 처리도 가능하면서 데이터가 갑자기 많아지더라도 확장이 용이한 시스템을 개발

**To - Be**
- 중추신경처럼, 한 군데에 모였다가 다시 퍼지는 구조로 변경
  이를 위해, 프로듀서와 컨슈머를 분리
- 메시지 데이터를 여러 컨슈머에 허용함으로써, 어떤 데이터가 카프카에 들어간 이후에는 여러 번 사용 가능
- 높은 처리량을 위해 메시지를 최적화
- 스케일 아웃 가능  
  ** 카프카의 클러스터를 만든 뒤에, 데이터가 많아져도 무중단으로 scale out 가능  
- 관련 생태계를 매우 다양하게 제공

### Kafka Broker & Cluster

**1. Kafka Broker**
- 실행된 카프카 애플리케이션 서버(중 한 대)
  Kafka 애플리케이션이 서버에 두 대 이상 뜰 수는 있음
  실제로 위와 같이 운영하는 경우는 거의 없음
- 3대 이상의 브로커로 클러스터 구성
- Stable 버전으로 ??? 확인!!
- 주키퍼와 연동 ( ~ 2.5.0버전 )  
  향후 주키퍼와의 분리를 목표로 로드맵을 가져가고 있음  
  주키퍼의 역할 : 메타 데이터(브로커 ID, 컨트롤러 ID 등) 저장
- n개의 브로커 중 1대는 컨트롤러(Controller) 기능 수행  
  컨트롤러 : 각 브로커에게 담당 파티션 할당 수행  
  브로커 정상 동작 모니터링 관리  
  누가 컨트롤러인지는 주키퍼에 저장

**Record**
- 어떤 데이터를 보는지, 프로듀서 레코드 : 토픽, 키, 메세지를 정함
- 토픽 : 데이터가 보내지는 특정 테이블처럼 저장소로 볼 수 있음
- 컨슈머 레코드를 통해서 토픽의 데이터를 다시 레코드로 받아옴
- 레코드도 key와 value로 되 형태로 받아옴
- 객체를 프로듀서에서 컨슈머로 전달하기 위해, Kafka 내부에 Byte형태로 저장할 수 있도록 직렬화/역직렬화하여 사용
- 기본 제공 직렬화 class : StringSerializer, ShortSerializer
- pull할 때와 push할 때 직렬화/역직렬화를 잘 맞춰줘야 함

**TOPIC & Partition**
- 토픽의 파티션은 1개 이상이 반드시 존재
- 파티션 0번 내 숫자가 또 있음(Offset이 붙음) -> 0이 가장 오래 된 것(First In, First Out -> 큐)
- 각 메시지 처리 순서는 파티션 별로 유지 관리 됨  
<br>

프로듀서는 레코드를 생성하여 브로커로 전송
- 프로듀서는 파티션의 오프셋이 지정된 레코드들을 각각 가져감
- 각각의 다른 기능을 가진 컨슈머는 동일 데이터를 여러 번 가져갈 수 있음
- 컨슈머는 브로커로부터 레코드를 요청하여 가져감(Polling)
- 이렇게 저장된 레코드는 파일 시스템 단위로 저장
- 카프카가 실제 파일로 저장
- 메시지가 저장될 때는 세그먼트 파일이 열려 있음
- 세그먼트 파일은 시간 또는 크기 기준으로 닫힘
- 닫힌 이후로는 일정 시간(또는 용량)에 따라 삭제(delete) 또는 압축(compact)
- 세그먼트로 적재된 레코드들은 일정 시간이나 용량 뒤에 삭제가 되면 더이상 레코드를 사용할 수 없음
- 카프카에 들어간 레코드는 영원하게도 사용할 수 있으나, 보통 용량이나 일정에 제한을 두므로 삭제될 수 있음

<br>

**If**, 파티션이 3개인 토픽  
- 1개의 프로듀서가 토픽에 레코드를 보내는 중
- 1개의 컨슈머가 3개의 파티션으로부터 polling 중
- 만약, 토픽이 3개 - 컨슈머가 3개인 경우는 1대 1 매칭이 됨  
  컨슈머는 각 파티션의 데이터를 가져감  
  토픽에 있는 모든 파티션이 할당되고, 컨슈머는 같이 일을 하게 됨  
  컨슈머는 결국 데이터를 처리할 때, 컨슈머 1대 당 처리 시간이 한정적인데,   
  각 파티션의 데이터를 여러 컨슈머가 처리하면 더욱 빠른 속도로 작업이 진행 됨

<br>

컨슈머 개수는 파티션 개수 이하로 생성
- 만약 컨슈머 갯수가 파티션 갯수보다 많아지면, 남은 컨슈머는 파티션을 할당받지 못하고 대기
- 컨슈머 중 한 개가 장애가 난 경우, 대비 가능 
  -> 리밸런스 발생 : 파티션 컨슈머 할당 재조정 ( 나머지 컨슈머가 파티션으로부터 polling 수행 )
  -> ex. 컨슈머 1 2 3 중 2번이 장애 발생 -> 컨슈머 1이 2개의 파티션에 할당이 됨  
  -> 모든 파티션이 끝까지 재할당되는 과정 : 리밸런싱  

<br>

**If**, 2개 이상의 컨슈머 그룹이 있을 경우
- 목적에 따라 컨슈머 그룹을 분리할 수 있음
- 장애 대응을 위해서, 임시 컨슈머 그룹을 생성할 수도 있음( 장애에 대응하기 위해 재입수(또는 재처리) 목적)

<br>

**If Case**, Application Log 적재 상황
- 엘라스틱서치 : 로그 실시간 확인용, 시간 순 정렬
(엘라스틱 서치의 컨슈머를 통해서 적재 가능 -> 키바나를 통해서, 검색하며 데이터를 볼 수 있음)
- 하둡 : 대용량 데이터 적재, 이전 데이터 확인용 (Long Term 데이터 확인용)

<br>

**If**, 각 컨슈머 그룹은 장애에 격리되는 다른 컨슈머 그룹
- 컨슈머 그룹 간 간섭(Coupling) 줄임
- 하둡에 이슈가 발생하여, 컨슈머의 적재 지연이 발생하더라도, 엘라스틱 서치에 적재하는 컨슈머의 동작에는 이슈가 없음

<br>

**Broker Partiion Replication**
```bash
$ bin/kafka-topics.sh --bootstrap-server loacalhost:9092 --create --topic topic_name --partitions 3
```
- 카프카의 토픽을 생성(kafka-topics.sh)
  sh : shell script -> 카프카 토픽을 생성하거나, 리스트를 보거나, 수정
  --bootstrap-server : 로컬 호스트에 떠져있는 카프카에 명령을 내린다
  --create : topic 생성
  topic_name : topic 이름 설정
  --partitions 3 : 파티션 개수 지정 (브로커에 균등하게 설정한 수만큼 파티션이 생성됨)

<br>

**If**, 브로커 1이 복구되기 전까지 Partition 1을 사용 불가
- Q. 카프카 브로커 이슈에 대응하기 위해, 사용할 수 있는 방법은?  
```bash
$ bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic topic_name --partitions3 --replication-factor 3
```
- A.  Partition을 다른 Broker에 복제(**Replication**)하여 이슈 대응  
  ex. 1번 Broker에 이슈가 발생하면, 다른 Broker에 복제된 데이터를 사용 

- --replication-factor 3 : 레플리케이션 개수 설정  
-> 기본 설정으로 --replication-factor 3으로 많이 운영  
-> 고 가용성을 위한 파티션 복제 기능으로 데이터 유실 방지


### 리더 파티션, 팔로워 파티션
- 리더 파티션 : Kafka 클라이언트와 데이터를 주고받는 역할
  Kafka 컨슈머나 프로듀서가 데이터를 직접 주고받음
- 팔로워 파티션 : 리더 파티션으로부터 레코드를 지속 복제(복제하는데 시간 소요)
- 리더 파티션의 동작이 불가능할 경우, 나머지 팔로워 중 1개가 리더로 선출됨

### ISR, 리더와 팔로워의 싱크
 - 파티션 3개, 레프리케이션 3개로 이루어진 토픽이 브로커에 할당된 모습
   - Broker #1 = Partition #1 + (Partition #2(Repl)) + (Partition #3(Repl))
   - Broker #2 = (Partition #1(Repl)) + Partition #2 + (Partition #3(Repl))
   - Broker #3 = (Partition #1(Repl)) + (Partition #2(Repl)) + Partition #3

<br>

- 특정 파티션의 리더, 팔로워가 레코드가 모두 복제되어 Sync가 맞는 상태 => ISR(In-Sync-Replica)
- 리더 파티션의 오프셋이 0~100까지 있는데, 나머지 팔로워 파티션에 모두 복제가 된 상태 : ISR
- 만약, 팔로워 파티션이 0~90까지만 복제되어있으면, 91~100번까지는 팔로워 파티션에 복제가 안된 상태
  -> 리더 파티션에 장애가 나면 복제 할 때까지 기다리거나 복제 안 하고 처리하는 방법 2가지로 나눔
  -> 이 방법을 선택하는 게 아래 옵션 unclean.leader.election.enable  
- ISR이 아닌 상태에서 장애가 나면 => unclean.leader.election.enable  
  "ISR이 아닌 리더 파티션을 선출해라"  
  -> false 상태 : 복제가 모두 될 때까지 기다렸다가 처리 (default)  
  -> true 상태 : 데이터 유실 감수하고 처리 먼저 진행  
  -> kafka client 와 연계된 내용

<br>

**If**, Broker #1 장애 발생 시,
- partition #1의 리더가 Broker #1 또는 #2 중에 새로 할당
- Kafka Client는 새로운 Partition 리더와 연동


### Kafka Rack-Awareness (참고)
- Server Rack : 한 개의 파워로 구성
 렉이 한 번 내려가면, 여러 서버가 한 번에 내려가게 됨  
 -> 1개의 Rack에는 1개의 Broker로 구성  
 -> 다수의 Rack에 분산하여 Broker 옵션(broker.rack) 설정 및 배치  
 -> 파티션 할당 및 레플리케이션 동작 시, 특정 Broker에 몰리는 현상 방지

 ### 왜 카프카 클러스터는 서버 장애에 대응한 로직이 많은지?
 - 서비스 운영에 있어서 장애 허용(Fault-Tolerant)은 아주 중요
 - 서버의 중단(이슈 발생, 재시작)은 언제든 발생할 수 있음
   ex. 30대 브로커로 이루어진 카프카 클러스터가 있을 때,  
   1대의 서버가 365일 중 1일 중단이 발생할 가능성이 있다고 가정하면 12.1일(약 2주)에 한 번씩 브로커 이슈 발생 가능
- 일부 서버가 중단되더라도 데이터가 유실되면 안 됨,  
  -> 안정성이 보장되지 않으면, 신뢰도가 하락(사용 중단)


## Kafka 핵심 요소
- Broker : 카프카 애플리케이션 서버 단위
- Topic : 데이터 분리 단위, 다수 파티션 보유
- Partition : 레코드를 담고 있음. 컨슈머 요청 시, 레코드 전달
- Offset : 각 레코드 당 파티션에 할당된 고유 번호
- Consumer : 레코드를 Polling 하는 애플리케이션
- Consumer Group : 다수 컨슈머 묶음
- Consumer Offset : 특정 컨슈머가 가져간 레코드의 번호 (컨슈머가 다음에 가져갈 Offset 체크 가능)
- Producer : 레코드를 브로커로 전송하는 애플리케이션
- Replication : 파티션 복제 기능
- ISR : 리더 + 팔로워 파티션의 Sync가 된 묶음
- Rack-awareness : Server Rack 이슈에 대응

## 관련 생태계
### Kafka Client
- Kafka와 데이터를 주고받기 위해, 사용하는 Java Library
- Producer, Consumer, Admin, Stream 등 Kafka 관련 API 제공
- 다양한 3rd party library 존재 : C/C++ , Node.js, Python, .Net 등
- Kafka Broker 버전과 Client 버전 하위호환 확인 필요

### Kafka Streams
- LINE이나 대기업에서는 쓰는 곳이 있음
- 다양한 데이터를 변환(Transformation)하기 위한 목적으로 사용하는 API
- 스트림 프로세싱을 지원하기 위한 다양한 기능을 제공
- Stateful 또는 Stateless와 같이 상태 기반 스트림을 통해서, Exactly-Once 즉 장애가 나더라도 각각의 Offset 레코드를 한 번씩만 처리하는 고가용성 특징
- Kafka Security(aci, sasl 등) 완벽 지원
- 스트림 처리를 위한 별도 Cluster(ex. Yarn 등) 불필요 -> Java Application으로 돌아감

### Kafka Connect
- 사실 Java로 Kafka Client에 Producer나 Consumer에 직접 다 구현해도 괜찮음  
  하지만, Kafka Connect를 사용하면 미리 제공된 Import/Export Application  
  이를 통해, Source System으로부터 Target 시스템으로 데이터를 거쳐갈 수 있음  
  코드 없이 Configuration으로 데이터를 이동시키는 것이 목적
- Standalone Mode, Distribution Mode 지원
- REST API Interface를 통해 제어
  즉, POST나 GET 등 HTTP 통신을 통해 제어 가능
- Stream 또는 Batch 형태로 데이터 전송 가능
- 커스텀 Connector를 통한 다양한 Plugin 제공(File, S3, Hive, MySQL, 등)

### Kafka Mirror Maker
- Kafka Source Cluster와 Kafka Target Cluster 간 Topic 전송
- 특정 카프카 클러스터에서 다른 카프카 클러스터로 Topic 및 Record를 복제하는 Standalone Tool
- 2019년 11월, 기존 MirrorMaker를 개선한 MirrorMaker2.0 Release
- 클러스터 간 토픽에 대한 모든 것을 복제하는 것이 목적
  - 신규 토픽, 파티션 감지 기능 및 토픽 설정 자동 Sync 기능
  - 양방향 클러스터 토픽 복제
  - 미러링 모니터링을 위한 다양한 metric(latency, count 등) 제공
  

### 그 외 Kafka 생태계를 지탱하는 Application 들
- confluent/ksqlDB : sql 구문을 통한 stream data processing 지원
- confluent/Schema Registry : avro 기반의 스키마 저장소
- confluent/REST Proxy : REST API 를 통한 Consumer/producer를 넣고 빼고 할 수 있음
- linkedin/Kafka burrow : consumer lag 수집 및 분석
- yahoo/CMAK : 카프카 클러스터 매니저
- uber/uReplicator : 카프카 클러스터 간 토픽 복제(전달)
- Spark stream : 다양한 소스(카프카 포함)로 부터 실시간 데이터 처리
- 일부 오픈소스의 경우 라이센스 이슈 확인 필요