# Kafka Installation
#1. Based on **Oracle VirtualBox**

## Installing Tool
1. VirtualBox 
   - 오라클 버추얼 박스 다운로드 : https://www.virtualbox.org/
   - 


## Setting
1. VM 생성 (server01 먼저 설정 후에 복사 -> /etc/sysconfig/network-scripts/ifcfg-eth0 설정만 각각에 맞춰서 변경)
  - vi /etc/sysconfig/network-scripts/ifcfg-eth0
   ```shell
   DEVICE=eth0
   HWADDR= {virtualbox 설정-네트워크-어댑터 2-MAC 주소를 2글자씩 :로 구분하여 작성}
   TYPE=Ethernet
   ONBOOT=yes
   BOOTPROTO=static
   IPADDR=192.168.56.101
   NETMASK=255.255.255.0
   GATEWAY=192.168.56.1
   NETWORK=192.168.56.0
   ```
  - vi /etc/udev/rules.d/70-persistent-net.rules 파일 열고, 주석 처리하라는데 파일이 없음

  - 방화벽 내리기
  ```bash
  systemctl stop firewalld
  yum install iptables-services -y
  systemctl stop iptables
  chkconfig iptables off
  chkconfig ip6tables off
  
  #혹은 firewall-cmd를 활용하여 설정
  ```

  - 기본 부팅 모드 (CUI 모드로 변경하기)
  ```bash
  unlink /etc/systemd/system/default.target
  ln -sf /lib/systemd/system/multi-user.target /etc/systemd/system/default.target
  #만약 gui 모드로 원하면
  #ln-sf /lib/systemd/system/graphical.target /etc/systemd/system/default.target
  ```

  - 호스트 네임 설정
  ```bash
  # server01에서
  hostnamectl set-hostname server01
  # server02에서
  hostnamectl set-hostname server02
  # server03에서
  hostnamectl set-hostname server03
  ```


  - 참고용
  * 클라우데라 Manager  설치
   https://drive.google.com/file/d/1oLikMIC6bzt0jNV0n49YNOM0foNPXDZ/view?usp=sharing
   -> 다운로드가 완료된 파일명은 Pilot Project VM.zip -> 압축해제 -> VM 에 있음

   * Kafka 설치 참고1 : https://shonm.tistory.com/644
   * Kafka 설치 참고2 : http://eg3020.blogspot.com/2020/09/apache-kafka-2.html
   * Kafka 설치 참고3 : https://bkjeon1614.tistory.com/634
   * Kafka 설치 참고4 : https://sh-safer.tistory.com/42
   * Kafka 설치 참고5 : https://hgko1207.github.io/2020/09/28/linux-4/
   * Kafka 설치 참고6 : https://m.blog.naver.com/firstpcb/221677456159

## Installing Local(VM)
### 1. Zookeeper
   - 설치와 환경설정 모두 3대 서버 동일하게 진행한다. 
   - 주키퍼는 과반수투표 프로세스 때문에 3대 5대 7대와 같이 홀수로 구성해야 한다.
   - http://apache.mirror.cdnetworks.com/zookeeper/  ← 옆 사이트로 접속하여, 사용할 zookeeper 버전 별 파일 확인
   - 설치한 파일 : http://apache.mirror.cdnetworks.com/zookeeper/zookeeper-3.6.3/apache-zookeeper-3.6.3-bin.tar.gz
     cf. apache-zookeeper-3.5.9.tar.gz 설치 시, FAILED TO START 에러 발생 → ~-3.6.3-bin.tar.gz 받아서 해결
  
2.1 zookeeper를 설치하기 위해, 먼저 java-1.8.0 설치
  ```bash
  # 설치가능한 OpenJDK 목록 확인
  yum list java*jdk-devel
  
  #OpenJDK 설치
  yum install java-1.8.0-openjdk-devel.x86_64 -y
  
  #설치된 javac확인
  javac -version

  #호스트 이름 확인
  vi /etc/hosts
  ```

  - vi /etc/hosts 안에 아래 세 줄을 모두 작성(3대 서버 모두)
  {1번 서버 IP주소}    {1번 서버 호스트네임}
  {2번 서버 IP주소}    {2번 서버 호스트네임}
  {3번 서버 IP주소}    {3번 서버 호스트네임}

  
  - 주키퍼와 카프카를 위한 방화벽 설정
  ```bash
  ## 주키퍼 포트
  firewall-cmd --permanent --zone=public --add-port=2181/tcp
  firewall-cmd --permanent --zone=public --add-port=2888/tcp
  firewall-cmd --permanent --zone=public --add-port=3888/tcp

  ## 카프카 포트
  firewall-cmd --permanent --zone=public --add-port=9092/tcp

  ## 방화벽 재시작
  firewall-cmd --reload
  ```


2.2 주키퍼 설치 진행
  ```bash
  # 설치할 path로 이동한다.
  cd /usr/local
  
  # zookeeper 파일 가져오기
  wget http://apache.mirror.cdnetworks.com/zookeeper/zookeeper-3.6.3/apache-zookeeper-3.6.3-bin.tar.gz

  tar -xzf apache-zookeeper-3.6.3-bin.tar.gz

  # 심볼릭 링크 생성 (Link파일 만드는 것)
  # ln -s (ln : 링크 생성, -s: 심볼릭 링크, 명령어 : ln -s {실제 폴더 혹은 파일명} {축약해서 쓸 이름})
  ln -s apache-zookeeper-3.6.3-bin zookeeper
  ```


  - 설치경로와른 다른 별도의 주키퍼와 카프카 데이터 디렉토리를 추가한다. 
  - 여기엔 주키퍼지노드 복사본인 스냅샷과 트랜잭션 로그들이 저장된다. 
  ```bash
  #server01 에서 
  mkdir -p /data/zookeepr1
  mkdir -p /data/kafka1
  #server02 에서
  mkdir -p /data/zookeepr2
  mkdir -p /data/kafka2
  #server03 에서
  mkdir -p /data/zookeepr3
  mkdir -p /data/kafka3
  ```

- Zookeeper의 노드 구분 ID 생성
  ``` bash
  # myid라는 파일을 만들고 내용을 각 서버 별로 1, 2, 3 이라고 줍니다.
  # server01에서 
  echo 1 > /data/zookeeper1/myid
  #server02에서
  echo 2 > /data/zookeeper2/myid
  #server03에서
  echo 3 > /data/zookeeper3/myid
  ```

- Zookeeper 설정 파일 수정
  ```bash
  # zookeeper 설정 파일 변경
  # 위에 링크(ln -s) 안 해놨으면 -> cd /usr/local/apache-zookeeper-3.6.3-bin/conf
  cd /usr/local/zookeeper/conf/
  cp ./zoo_sample.cfg ./zoo.cfg
  vi /usr/local/zookeeper/conf/zoo.cfg
  

  # Server01 에서 vi /usr/local/zookeeper/conf/zoo.cfg 
  dataDir=/data/zookeeper1 #수정
  server.1=server01:2888:3888 #추가
  server.2=server02:2888:3888 #추가
  server.3=server03:2888:3888 #추가

  # Server02 에서 vi /usr/local/zookeeper/conf/zpp.cfg 
  dataDir=/data/zookeeper2 #수정
  server.1=server01:2888:3888 #추가
  server.2=server02:2888:3888 #추가
  server.3=server03:2888:3888 #추가

  # Server03 에서 vi /usr/local/zookeeper/conf/zpp.cfg 
  dataDir=/data/zookeeper3 #수정
  server.1=server01:2888:3888 #추가
  server.2=server02:2888:3888 #추가
  server.3=server03:2888:3888 #추가
  ```

- 설정 설명
  - tickTime=2000 : 주키퍼가 사용하는 시간에 대한 기본단위(밀리초), heartbeats를 보내는데 사용
                    또한 세션 타임아웃 최소 단위는 tickTime의 2배로 설정
  - initLimit=10 : 팔로워가 리더와 초기에 연결하는 시간에 대한 타임아웃 .tick의 수
                   Zookeeper 서버들이 Leader에 연결할 때, 사용되는 최대 시간을 제한하기 위해 사용하는 timeout 단위
  - syncLimit=5 : 팔로워가 리더와 동기화하는 시간에 대한 타임아웃 tick의 수
                  (주키퍼에 저장된 데이터가 크면 수를 늘려야 함)
                  서버가 Leader로부터 얼마나 Sync에 뒤처질 수 있는지를 제한하는 Timeout 단위
  - dataDir : 주키퍼의 트랜잭션 로그와 스냅샷이 저장되는 데이터 저장경로
              인메모리 데이터베이스 스냅샷을 저장할 공간.
              특정 directory가 명시되지 않으면, 트랜잭션 로그는 database에 기록된다
  - clientPort=2181 : 주키퍼 사용 TCP포트, Client의 연결을 Listen할 Port 번호
  - maxClientCnsxns=60 : 하나의 클라이언트에서 동시접속하는 수 제한. 0이면 unlimit(무제한)로 설정, 기본값은 60
  - autopurge.purgeInterval=1 : 스냅샷 및 해당 트랜잭셕로그 자동 삭제 주기. 양수(1이상)로 설정하면 ON, 0은 OFF
  - server.N : 주기퍼 앙상플 구성을 위한 설정
  - server.(myid 의 id)= 서버 아이피 : peer 와 peer 끼리 연결 포트 : leader를 선출하기 위한 투표 포트
  - 원래 peer 연결 포트와 leader 선출 포트는 각 서버마다 동일하게 설정
  - 2888, 3888은 기본 포트이며 앙상블 내 노드끼리 연결(2888)하고, 리더선출(3888)에 사용한다.
  - cf. 동일 서버에 모두 설치할 경우, 다르게 설정함
     - ex. server.1=192.168.122.1:28881:38881
           server.2=192.168.122.1:28882:38883
           server.3=192.168.122.1:28883:38883

- zookeeper 실행/중지
  ```bash
  # 주키퍼 설정 확인
  cd /usr/local/zookeeper/bin/

  # Tip) .sh 파일은 Unix에서 실행, .cmd 파일은 MSDOS/Windows에서 실행
  # 주키퍼 실행
  /usr/local/zookeeper/bin/zkServer.sh start
  # 출력값
  /usr/bin/java
  ZooKeeper JMX enabled by default
  Using config: /usr/local/zookeeper/bin/../conf/zoo.cfg
  Starting zookeeper ...STARTED

  # 주키퍼 정지
  /usr/local/zookeeper/bin/zkServer.sh stop
  ```

#### Zookeeper 확인
- 카프카 브로커 서버들과 주키퍼 서버와 통신 가능 유무 확인
- nc -v IP주소 Port 번호
  ```bash
  # 포트가 막혀있으면 포트 설정
  # 3개 노드 어디서든 아래 모든 명령어가 실행 가능 
  # Connected to {IP}:2181이 뜨면 성공
  nc -v 192.168.56.101 2181
  nc -v 192.168.56.102 2181
  nc -v 192.168.56.103 2181
  ```

### 2. Kafka
#### 1. Kafka 환경설정
- 카프카 클러스터의 브로커 수를 3대로 구성
- 카프카 또한 자바 애플리케이션으로 자바가 설치되어야 함.
```bash
$ cd /usrl/local
$ wget http://mirror.navercorp.com/apache/kafka/2.6.0/kafka_2.13-2.6.0.tgz
$ tar zxf kafka_2.13-2.6.0.tgz

#심볼릭 링크
ln -s kafka_2.13-2.6.0
```

- 카프카 환경설정
  - 서버별 브로커 아이디
  - 카프카 저장 디렉토리
  - 주키퍼정보

  - 서버별 브로커 아이디
    호스트        브로커ID
    hadoop01    broker.id=1
    hadoop02    broker.id=2
    kadoop03    broker.id=3

- 카프카 저장디렉토리
  - 카프카는 컨슈머가 메세지 소비 후에도 저장된 데이터를 임시로 보관할 수 있다.
  - 이 데이터들은 디스크마다 별도로 저장할 수 있는데 예제에서는 디렉토리로 대체한다.
  
  ```bash
  
  $ mkdir -p /data
  $ mkdir -p /data
  ```
  
- 주키퍼정보
  - zookeeper.connect=주키퍼호스트:주키퍼포트/지노드네임
  - zookeeper.connect=172.30.1.17:2181,172.30.1.59:2181,172.30.1.40:2181/hadoop-kafka

- server.properties 파일을 열어 3대 모두 카프카 환경설정을 해준다.
 ```bash
 $ vi /usr/local/kafka/config/server.properties
 ```

- broker.id = 1 / 2 / 3     각 서버별로 다르게 
- log.dirs=/data1,/data2
- zookeeper.connect=hadoop01:2181,hadoop02:2181,hadoop03:2181/hadoop-kafka


#### 2. Kafka 실행
--daemon 옵션을 주어 백그라운드로 실행한다.
```bash
$/usr/local/kafka/bin/kafka-server-start.sh -daemon /usr/local/kafka/config/server.properties
```

#### 실행 확인
- TCP 포트 확인
  ```bash
  #주키퍼
  netstat -ntlp | grep 2181
  #결과 : tcp6 0 0 :::2181 :::* LISTEN  1954/java

  #카프카
  netstat -ntlp | grep 9092
  #결과 : tcp6 0 0 :::9092 :::* LISTEN  2205/java
  ```

----------------------------------------

# 2. Kubernetes 에서 설치하기 (with ELK)
- 참고 : https://llnote.tistory.com/679
- 참고 : https://blog.naver.com/PostView.nhn?blogId=priince&logNo=221401506828
- (helm이용) 참고 : https://bonahbruce.tistory.com/95?category=871281

## 1. Kubernetes 설치
-> 설치 되어있음

## 2. Docker 설치하기
```bash
#예전 버전 지우기 (없었지만, 혹시 모르니까)
sudo yum remove docker
                docker-client
                docker-client-latest
                docker-common
                docker-latest
                docker-latest-logrotate
                docker-logrotate
                docker-engine

sudo yum install -y yum-utils
yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
yum install docker-ce docker-ce-cli containerd.io
systemctl enable docker
systemctl start docker
sudo mkdir /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

systemctl daemon-reload
systemctl restart docker
```

## 3. ELK 설치하기
- ECK 설치
  ```bash
  kubectl apply -f https://download.elastic.co/downloads/eck/1.2.1/all-in-one.yaml
  ```

- ECK 로그 확인
  ```bash
  kg all -n elastic-system


-------
-------

# Kubernetes - ZOOKEEPER
[root@k8s-worker08 ~]# kg po -n zk-g1
NAME   READY   STATUS    RESTARTS   AGE
zk-0   1/1     Running   0          9m11s
zk-1   1/1     Running   0          8m33s
zk-2   1/1     Running   0          8m6s
[root@k8s-worker08 ~]# kg po --help
Display one or many resources

 Prints a table of the most important information about the specified resources. You can filter the list using a label
selector and the --selector flag. If the desired resource type is namespaced you will only see results in your current
namespace unless you pass --all-namespaces.

 Uninitialized objects are not shown unless --include-uninitialized is passed.

 By specifying the output as 'template' and providing a Go template as the value of the --template flag, you can filter
the attributes of the fetched resources.

Use "kubectl api-resources" for a complete list of supported resources.

Examples:
  # List all pods in ps output format.
  kubectl get pods

  # List all pods in ps output format with more information (such as node name).
  kubectl get pods -o wide

  # List a single replication controller with specified NAME in ps output format.
  kubectl get replicationcontroller web

  # List deployments in JSON output format, in the "v1" version of the "apps" API group:
  kubectl get deployments.v1.apps -o json

  # List a single pod in JSON output format.
  kubectl get -o json pod web-pod-13je7

  # List a pod identified by type and name specified in "pod.yaml" in JSON output format.
  kubectl get -f pod.yaml -o json

  # List resources from a directory with kustomization.yaml - e.g. dir/kustomization.yaml.
  kubectl get -k dir/

  # Return only the phase value of the specified pod.
  kubectl get -o template pod/web-pod-13je7 --template={{.status.phase}}

  # List resource information in custom columns.
  kubectl get pod test-pod -o custom-columns=CONTAINER:.spec.containers[0].name,IMAGE:.spec.containers[0].image

  # List all replication controllers and services together in ps output format.
  kubectl get rc,services

  # List one or more resources by their type and names.
  kubectl get rc/web service/frontend pods/web-pod-13je7

Options:
  -A, --all-namespaces=false: If present, list the requested object(s) across all namespaces. Namespace in current
context is ignored even if specified with --namespace.
      --allow-missing-template-keys=true: If true, ignore any errors in templates when a field or map key is missing in
the template. Only applies to golang and jsonpath output formats.
      --chunk-size=500: Return large lists in chunks rather than all at once. Pass 0 to disable. This flag is beta and
may change in the future.
      --field-selector='': Selector (field query) to filter on, supports '=', '==', and '!='.(e.g. --field-selector
key1=value1,key2=value2). The server only supports a limited number of field queries per type.
  -f, --filename=[]: Filename, directory, or URL to files identifying the resource to get from a server.
      --ignore-not-found=false: If the requested object does not exist the command will return exit code 0.
  -k, --kustomize='': Process the kustomization directory. This flag can't be used together with -f or -R.
  -L, --label-columns=[]: Accepts a comma separated list of labels that are going to be presented as columns. Names are
case-sensitive. You can also use multiple flag options like -L label1 -L label2...
      --no-headers=false: When using the default or custom-column output format, don't print headers (default print
headers).
  -o, --output='': Output format. One of:
json|yaml|wide|name|custom-columns=...|custom-columns-file=...|go-template=...|go-template-file=...|jsonpath=...|jsonpath-file=...
See custom columns [http://kubernetes.io/docs/user-guide/kubectl-overview/#custom-columns], golang template
[http://golang.org/pkg/text/template/#pkg-overview] and jsonpath template
[http://kubernetes.io/docs/user-guide/jsonpath].
      --output-watch-events=false: Output watch event objects when --watch or --watch-only is used. Existing objects are
output as initial ADDED events.
      --raw='': Raw URI to request from the server.  Uses the transport specified by the kubeconfig file.
  -R, --recursive=false: Process the directory used in -f, --filename recursively. Useful when you want to manage
related manifests organized within the same directory.
  -l, --selector='': Selector (label query) to filter on, supports '=', '==', and '!='.(e.g. -l key1=value1,key2=value2)
      --server-print=true: If true, have the server return the appropriate table output. Supports extension APIs and
CRDs.
      --show-kind=false: If present, list the resource type for the requested object(s).
      --show-labels=false: When printing, show all labels as the last column (default hide labels column)
      --sort-by='': If non-empty, sort list types using this field specification.  The field specification is expressed
as a JSONPath expression (e.g. '{.metadata.name}'). The field in the API resource specified by this JSONPath expression
must be an integer or a string.
      --template='': Template string or path to template file to use when -o=go-template, -o=go-template-file. The
template format is golang templates [http://golang.org/pkg/text/template/#pkg-overview].
  -w, --watch=false: After listing/getting the requested object, watch for changes. Uninitialized objects are excluded
if no object name is provided.
      --watch-only=false: Watch for changes to the requested object(s), without listing/getting first.

Usage:
  kubectl get
[(-o|--output=)json|yaml|wide|custom-columns=...|custom-columns-file=...|go-template=...|go-template-file=...|jsonpath=...|jsonpath-file=...]
(TYPE[.VERSION][.GROUP] [NAME | -l label] | TYPE[.VERSION][.GROUP]/NAME ...) [flags] [options]

Use "kubectl options" for a list of global command-line options (applies to all commands).
[root@k8s-worker08 ~]# for i in 0 1 2; do kubectl exec -n zk-g1 zk-$i -- hostname; done
zk-0
zk-1
zk-2
[root@k8s-worker08 ~]# for i in 0 1 2; do echo "myid zk-$i";kubectl exec -n zk-g1 zk-$i -- cat /var/lib/zookeeper/data/myid; done
myid zk-0
1
myid zk-1
2
myid zk-2
3
[root@k8s-worker08 ~]# for i in 0 1 2; do kubectl exec -n zk-g1 zk-$i -- hostname -f; done
zk-0.zk-hs.zk-g1.svc.cluster.local
zk-1.zk-hs.zk-g1.svc.cluster.local
zk-2.zk-hs.zk-g1.svc.cluster.local
[root@k8s-worker08 ~]# kubectl exec -n zk-g1 zk-0 -- cat /opt/zookeeper/conf/zoo.cfg
#This file was autogenerated DO NOT EDIT
clientPort=2181
dataDir=/var/lib/zookeeper/data
dataLogDir=/var/lib/zookeeper/data/log
tickTime=2000
initLimit=10
syncLimit=5
maxClientCnxns=60
minSessionTimeout=4000
maxSessionTimeout=40000
autopurge.snapRetainCount=3
autopurge.purgeInteval=12
server.1=zk-0.zk-hs.zk-g1.svc.cluster.local:2888:3888
server.2=zk-1.zk-hs.zk-g1.svc.cluster.local:2888:3888
server.3=zk-2.zk-hs.zk-g1.svc.cluster.local:2888:3888
[root@k8s-worker08 ~]# kubectl get pods -w -l app=zk -n zk-g1
NAME   READY   STATUS    RESTARTS   AGE
zk-0   1/1     Running   0          11m
zk-1   1/1     Running   0          11m
zk-2   1/1     Running   0          10m


