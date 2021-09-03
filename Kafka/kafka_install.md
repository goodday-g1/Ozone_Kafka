# Kafka Installation
#1. Based on **Oracle VirtualBox**

### Installing Tool
1. VirtualBox 
   - 오라클 버추얼 박스 다운로드 : https://www.virtualbox.org/
   - 


### Setting
1. Server 01
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
  ```

  기본 부팅 모드 (CUI 모드로 변경하기)
  ```bash
  unlink /etc/systemd/system/default.target
  ln -sf /lib/systemd/system/multi-user.target /etc/systemd/system/default.target
  #만약 gui 모드로 원하면
  #ln-sf /lib/systemd/system/graphical.target /etc/systemd/system/default.target
  ```


- 참고용
  * 클라우데라 Manager  설치
   https://drive.google.com/file/d/1oLikMIC6bzt0jNV0n49YNOM0foNPXDZ/view?usp=sharing
   -> 다운로드가 완료된 파일명은 Pilot Project VM.zip -> 압축해제 -> VM 에 있음

   * Kafka 설치 참고1 : https://shonm.tistory.com/644
   * Kafka 설치 참고2 : http://eg3020.blogspot.com/2020/09/apache-kafka-2.html
   * Kafka 서치 참고3 : https://bkjeon1614.tistory.com/634


2. Zookeeper 설치
   - 설치와 환경설정 모두 3대 서버 동일하게 진행한다. 
   - 주키퍼는 과반수투표 프로세스 때문에 3대 5대 7대와 같이 홀수로 구성해야 한다.
   - http://apache.mirror.cdnetworks.com/zookeeper/  ← 옆 사이트로 접속하여, 사용할 zookeeper 버전 별 파일 확인
  
   - zookeeper를 설치하기 위해, 먼저 java-1.8.0 설치
  ```bash
  # 설치가능한 OpenJDK 목록 확인
  yum list java*jdk-devel
  
  #OpenJDK 설치
  yum install java-1.8.0-openjdk-devel.x86_64 -y
  
  #설치된 javac확인
  javac -version
  ```
  - 주키퍼 설치 진행
  ```bash
  # 설치할 path로 이동한다.
  cd /usr/local
  
  # zookeeper 파일 가져오기
  wget http://apache.mirror.cdnetworks.com/zookeeper/zookeeper-3.5.9/apache-zookeeper-3.5.9.tar.gz 

  tar -xzf apache-zookeeper-3.5.9.tar.gz

  # 심볼릭 링크 생성 (모르겠는 거 !! 공부해보쟈!!!!!)!!!!!!!!
  ln -s zookeeper-3.5.9 zookeeper
  ```


  - 설치경로와른 다른 별도의 주키퍼 데이터디렉토리를 추가한다. 
  - 여기엔 주키퍼지노드 복사본인 스냅샷과 트랜잭션 로그들이 저장된다. 
  ```bash
  mkdir -p /data
  
  #myid라는 파일을 만들고 내용을 1이라고 한다.
  echo 1> /data/myid    //host hadoop01
  echo 2> /data/myid    //host hadoop02
  echo 3> /data/myid    //host hadoop03

  #zookeeper 설정 파일 변경
  cd /usr/local/apache-zookeeper-3.5.9/conf
  vi zoo_sample.cfg
  ```

  - tickTime=2000 : 주키퍼가 사용하는 시간에 대한 기본단위(밀리초)
  - initLimit=10 : 팔로워가 리더와 초기에 연결하는 시간에 대한 타임아웃 tick의 수
  - syncLimit=5 : 팔로워가 리더와 동기화하는 시간에 대한 타임아웃 tick의 수 (주키퍼에 저장된 데이터가 크면 수를 늘려야 함)
  - dataDir : 주기퍼의 트랜잭션 로그와 스냅샷이 저장되는 데이터 저장경로
  - clientPort : 주키퍼 사용 TCP포트
  - maxClientCnsxns=60 : 하나의 클라이언트에서 동시접속 수 제한. 0이면 unlimit로 설정
  - autopurge.purgeInterval=1 : 스냅샷 및 해당 트랜잭셕로그 자동 삭제 주기. 양수(1이상)로 설정하면 ON, 0은 OFF
  - server.N : 주기퍼 앙상플 구성을 위한 설정






