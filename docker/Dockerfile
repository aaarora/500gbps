FROM opensciencegrid/software-base:fresh

ADD influxdb.repo /etc/yum.repos.d/influxdb.repo

RUN yum -y install vim && \
    yum -y install osg-xrootd-standalone --enablerepo=osg-upcoming && \
    yum -y install telegraf && \
    yum -y install http://uaf-10.t2.ucsd.edu/~aaarora/packages/osg-ca-generator-1.5.0.tar.gz

ADD image-config.d/* /etc/osg/image-config.d/
