FROM alpine:3.7

# Include dist
ADD dist/ /root/dist/

# Setup apt
RUN apk -U --no-cache add bash \
               build-base \
               cython-dev \
               file \
               git \
               libev \
               libtool \
               libcap \
               libxslt \
               libxslt-dev \
               mariadb-dev \
               mariadb-client-libs \
               pkgconfig \
               python \
               python-dev \
               py-cffi \
               py-cryptography \
               tcpdump \
               wget && \

# Setup ConPot
    git clone https://github.com/mushorg/conpot /opt/conpot/ && \
    cd /opt/conpot/ && \
    git checkout dc95c924050554d23544a890d76c5c06a7474b60 && \
    cp /root/dist/requirements.txt /opt/conpot/ && \
    cp /root/dist/snmp_server.py /opt/conpot/conpot/protocols/snmp/ && \
    cp /root/dist/conpot /opt/conpot/bin && \
    python setup.py install && \
    cd / && \
    cp /root/dist/conpot.bin /usr/bin/conpot && \
    chmod u+x /usr/bin/conpot && \
    rm -rf /opt/conpot /tmp/* /var/tmp/* && \
    setcap cap_net_bind_service=+ep /usr/bin/conpot && \

# Get wireshark manuf db for scapy, setup configs
    mkdir -p /etc/conpot /var/log/conpot /usr/share/wireshark && \
    wget https://github.com/wireshark/wireshark/raw/master/manuf -o /usr/share/wireshark/manuf && \
    cp /root/dist/conpot.cfg /etc/conpot/conpot.cfg && \
    cp -R /root/dist/templates /usr/lib/python2.7/site-packages/Conpot-0.5.1-py2.7.egg/conpot/ && \

# Clean up
    apk del --purge build-base \
            cython-dev \
            file \
            git \
            libev \
            libtool \
            libxslt-dev \
            mariadb-dev \
            pkgconfig \
            python-dev \
            py-cffi \
            wget && \
    rm -rf /root/* && \
    rm -rf /var/cache/apk/*

# Expose all possible ports
EXPOSE 80 102 161 502 623 1025 1026 1234 2404 10001 44818 47808 50100

# Start conpot
CMD /usr/bin/conpot --template $CONPOT_TEMPLATE --logfile $CONPOT_LOG --config $CONPOT_CONFIG
