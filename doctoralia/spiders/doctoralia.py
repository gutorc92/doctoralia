# -*- coding: utf-8 -*-
import scrapy
import json
from slugify import slugify
from doctoralia.items import Doctor

def get_phone(response):
    phone = ''
    phone = response.xpath('//*[@id="profile-info"]/div[2]/div[2]/div/div[1]/div[2]/div[7]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/a/@href').get()
    if not phone:
        phone = response.xpath('//*[@id="profile-info"]/div[2]/div[2]/div/div[1]/div[2]/div[3]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div/a/@href').get()
    return phone

def get_name(response):
    name = response.xpath('//*[@id="object-profile"]/div[1]/div[2]/main/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/div[3]/div/h1/div/span[2]/text()').get()
    if not name:
        name = response.xpath('//*[@id="object-profile"]/div[1]/div[2]/main/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/div[3]/div/h1/div/span/text()').get()
    return name

class DoctoraliaSpider(scrapy.Spider):
    name = 'doctoralia'
    allowed_domains = ['doctoralia.com.br']
    start_urls = ['https://www.doctoralia.com.br']

    BASE_URL = 'https://www.doctoralia.com.br'

    def parse(self, response):
        especialidades = json.loads(response.xpath('//*[@id="search"]/div/div[1]/template/@data-json').get())
        cities = json.loads(response.xpath('//*[@id="search"]/div/div[2]/template/@data-json').get())
        for city in cities:
            for especialidade in especialidades:
                absolute_url = self.BASE_URL + '/' +  slugify(especialidade.lower()) + '/' + slugify(city.lower())
                print(absolute_url)
                yield scrapy.Request(absolute_url, callback=self.parse_city_escialidade, meta={'city_name': city})
    
    def parse_city_escialidade(self, response):
        city_name = response.meta.get('city_name', '')
        doctors = response.xpath('//*[@id="search-content"]/div[2]/ul')
        page_doctors = doctors.xpath('.//li/div[1]/div/div/div[1]/div[1]/div[2]/h3/a/@href').extract()
        for page in page_doctors: 
            yield scrapy.Request(page, callback=self.parse_doctor, meta={'city_name': city_name})
    
    def parse_doctor(self, response):
        city_name = response.meta.get('city_name', '')
        doctor = Doctor()
        doctor['name'] = get_name(response)
        doctor['proficiency'] = response.xpath('//*[@id="object-profile"]/div[1]/div[2]/main/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/div[3]/div/h2/a/@title').get()
        doctor['phone'] = get_phone(response)
        doctor['score'] = response.xpath('//*[@id="object-profile"]/div[1]/div[2]/main/div[2]/div[1]/div[2]/div[1]/div/div[1]/div[1]/div/div[3]/div/a/span/@data-score').get()
        doctor['city'] = response.xpath('//*[@id="profile-info"]/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/h5/span[2]/@content').get()
        doctor['estate'] = response.xpath('//*[@id="profile-info"]/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/h5/span[3]/@content').get()
        doctor['url'] = response.url
        doctor['specialty'] = response.xpath('//*[@id="profile-info"]/div[3]/div[2]/div/div[3]/div[2]/ul/li/a/text()').extract()
        address = ''
        for element in response.xpath('//*[@id="profile-info"]/div[3]/div[2]/div/div[1]/div[2]/div[1]/div[2]/div/h5/span[5]'): 
            second_line = first_line =  ''
            try:
                second_line = element.xpath('.//a/text()').get().strip()
            except:
                pass
            try:
                first_line = element.xpath('.//span/text()').get().strip()
            except:
                pass
            address = first_line + second_line
        doctor['address'] = address
        yield doctor