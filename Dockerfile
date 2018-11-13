FROM registry.boyait.9fwealth.com:1443/devops/images/python:3.6-celery
ADD DevOpsPlatForm /work
WORKDIR /work/
EXPOSE 8000
# ENTRYPOINT ["bash", "manage.py", "runserver"]
CMD ["bash", "-c", "starh.sh"]