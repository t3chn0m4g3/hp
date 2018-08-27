FROM alpine:3.8

# Include dist
ADD dist/ /root/dist/

# Setup apt
RUN apk -U --no-cache add \
               build-base \
               file \
               git \
               libev \
               libtool \
               libcap \
               libxslt \
               libxslt-dev \
               mariadb-dev \
               pkgconfig \
               python3 \
               python3-dev \
               py-cffi \
               py-cryptography \
               tcpdump \
               wget && \

# Setup ConPot
    git clone --depth=1 https://github.com/mushorg/conpot /opt/conpot && \
    cd /opt/conpot/ && \
    cp /root/dist/requirements.txt /opt/conpot/ && \
    # Patch to accept ENV for MIB path
    cp /root/dist/snmp_server.py /opt/conpot/conpot/protocols/snmp/ && \
    # Change template default ports if <1024
    sed -i 's/port="2121"/port="21"/' /opt/conpot/conpot/templates/default/ftp/ftp.xml && \
    sed -i 's/port="8800"/port="80"/' /opt/conpot/conpot/templates/default/http/http.xml && \
    sed -i 's/port="6230"/port="623"/' /opt/conpot/conpot/templates/default/ipmi/ipmi.xml && \
    sed -i 's/port="5020"/port="502"/' /opt/conpot/conpot/templates/default/modbus/modbus.xml && \
    sed -i 's/port="10201"/port="102"/' /opt/conpot/conpot/templates/default/s7comm/s7comm.xml && \
    sed -i 's/port="16100"/port="161"/' /opt/conpot/conpot/templates/default/snmp/snmp.xml && \
    sed -i 's/port="6969"/port="69"/' /opt/conpot/conpot/templates/default/tftp/tftp.xml && \
    sed -i 's/port="16100"/port="161"/' /opt/conpot/conpot/templates/IEC104/snmp/snmp.xml && \
    sed -i 's/port="6230"/port="623"/' /opt/conpot/conpot/templates/ipmi/ipmi/ipmi.xml && \
    pip3 install --no-cache-dir -U pip setuptools && \
    pip3 install --no-cache-dir . && \
    cd / && \
    rm -rf /opt/conpot /tmp/* /var/tmp/* && \
    setcap cap_net_bind_service=+ep /usr/bin/python3.6 && \
    # Fix kamstrup not starting error / #398 Workaround
    ln -s /usr/lib/python3.6/site-packages/conpot/protocols/kamstrup/meter_protocol /usr/lib/python3.6/site-packages/conpot/protocols/kamstrup_meter && \
    ln -s /usr/lib/python3.6/site-packages/conpot/protocols/kamstrup/management_protocol /usr/lib/python3.6/site-packages/conpot/protocols/kamstrup_management && \
    
# Get wireshark manuf db for scapy, setup configs
    mkdir -p /etc/conpot /var/log/conpot /usr/share/wireshark && \
    wget https://github.com/wireshark/wireshark/raw/master/manuf -o /usr/share/wireshark/manuf && \
    cp /root/dist/conpot.cfg /etc/conpot/conpot.cfg && \
    cp -R /root/dist/templates /usr/lib/python3.6/site-packages/conpot/ && \

# Clean up
    apk del --purge \
            build-base \
            cython-dev \
            file \
            git \
            libev \
            libtool \
            libxslt-dev \
            mariadb-dev \
            pkgconfig \
            python3-dev \
            py-cffi \
            wget && \
    rm -rf /root/* && \
    rm -rf /var/cache/apk/*

# Expose all possible ports
EXPOSE 21 69 80 102 161 502 623 1025 1026 1234 2404 10001 44818 47808 50100

# Start conpot
STOPSIGNAL SIGINT
USER nobody:nobody
CMD exec /usr/bin/conpot --temp_dir $CONPOT_TMP --template $CONPOT_TEMPLATE --logfile $CONPOT_LOG --config $CONPOT_CONFIG
