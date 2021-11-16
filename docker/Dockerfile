FROM opensciencegrid/software-base:fresh

ADD influxdb.repo /etc/yum.repos.d/influxdb.repo

RUN yum -y install vim && \
    yum -y install osg-xrootd-standalone --enablerepo=osg-upcoming && \
    yum -y install telegraf && \
    yum -y install nvme-cli && \
    yum -y install xfsprogs

ADD osg-ca-generator-1.5.0.tar.gz /osg-ca-generator-1.5.0.tar.gz

RUN tar -xvf osg-ca-generator-1.5.0.tar.gz && \
    cd osg-ca-generator-1.5.0 && \
    make install

ADD image-config.d/* /etc/osg/image-config.d/
