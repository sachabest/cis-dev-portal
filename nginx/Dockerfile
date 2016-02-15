FROM matter/shibboleth-nginx
ADD nginx.conf /etc/nginx/
ADD default.conf /etc/nginx/conf.d/
ADD private.key /etc/nginx/conf/ssl.key
ADD shib3.xml /etc/shibboleth/shibboleth2.xml
ADD shib3.xml /etc/shibboleth/shibboleth2.xml.tpl
ADD sachabest.com.crt /etc/nginx/conf/sachabest.com.crt
EXPOSE 80 443 9090

CMD ["/usr/local/bin/ep", "-v", "/etc/nginx/conf.d/default.conf", "/etc/shibboleth/shibboleth2.xml", "--", "/usr/bin/supervisord", "--nodaemon", "--configuration", "/etc/supervisor/supervisord.conf"]