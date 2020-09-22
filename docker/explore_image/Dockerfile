FROM centos:7.8.2003 AS base

# Adjust timeZone
RUN cp -f /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
RUN yum install which

CMD [ "/bin/bash", "-c", "/bin/sleep 5000" ]
