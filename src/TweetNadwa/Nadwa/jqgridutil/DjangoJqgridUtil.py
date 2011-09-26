'''
Created on Mar 29, 2011

@author: aali
'''
import math
import logging
import time
from datetime import datetime
from django.utils import simplejson as json
from DjangoStuff import DjangoStuff
import logging
from django.http import HttpRequest as DjangoRequest
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.fields import NOT_PROVIDED
class Jqgrid():
	'''
	table  : the table object
	tableID: the col that will act as ID in the Grid
	'''
	def __init__(self, table, displayList = [], tableID = None):
		if issubclass(table, models.Model):
			self.table = table
			fields = self.table.__dict__['__doc__'].replace(' ','')
			fields = fields[fields.find('(')+1:len(fields)-1].split(',')
			fieldsType = self.table.__dict__['_meta'].__dict__['_field_name_cache']
			self.AllMembers = {}
			self.displayMembers = []
			
			for i in range(len(fields)):
				self.AllMembers[fields[i]] = fieldsType[i]
			
			if tableID and tableID in self.AllMembers.keys():
				self.displayMembers = [tableID]
				self.tableID = tableID
			else:
				self.tableID = 'id'
				self.displayMembers = [self.tableID]
			
			for mem in self.AllMembers.keys():
				if mem not in self.displayMembers:
					self.displayMembers.append(mem)
			self.moreTemplate = ''
			self.singleTemplate = ''
			self.buildTemplate(displayList)
			self.djangoStuff = DjangoStuff()
			self.entityErr = False
		else:
			self.entityErr = True
	
	def handler(self, request):
		if not self.entityErr:
			if isinstance(request, DjangoRequest):
				try:
					(page, limit, sidx, sord, search, filter, custom_search, custom_filter) = self.djangoStuff.readRequest_handler(request)
					return self._handler(page, limit, sidx, sord, search, custom_search, filter, custom_filter)
				except KeyError:
					return "Missing Request Object Elements"
			else:
				raise "UN-determine Request Object"
		else:
			return "Un-determine Entinty Class"
	'''
	page   : the number of page requested
	limit  : the number of rows that will display on the grid
	sidx   : the sorting col name or index
	sord   : the direction of sort asc or desc
	search : the flag to search
	filter : the set of cols and ops and data in JSON format
	'''
	def _handler(self, page, limit, sidx, sord, search, custom_search, filter = '', custom_filter = ''):
#		res = self.table.objects.count();
		res = None
		count = self.table.objects.count();
		if not sidx:
			sidx = 1
		if count > 0:
			total_pages = int(math.ceil(count / float(limit) ) )
		else:
			total_pages = 0
		if page > total_pages:
			page = total_pages
		start = ( limit * page ) - limit
		if sord == 'desc':
			sidx = '-%s'%sidx
		if search == 'true' or custom_search == 'true':
			if custom_search == 'true':
				groupOp = custom_filter['groupOp']
			if search == 'true':
				groupOp = filter['groupOp']
				
			rules = []
			if search == 'true':
				rules = filter['rules']
			if custom_search == 'true':
				rules.append(custom_filter['rules'][0])
#			print 'GroupOp = %s' %groupOp
#			print 'Rules = %s ' %rules
#			sidx = rules[0]['field']
#			if sord == 'desc':
#				sidx = '-%s'%sidx
			ops = { 'eq' : "" ,
					'lt' : '__lt',
					'le' : '__lte',
					'gt' : '__gt',
					'ge' : '__gte',
					'bw' : '__startswith',
					'be' : '__istartswith',
					'ew' : '__endswith',
					'cn' : '__contains',
					'nc' : '__icontains',
				}
			if groupOp == 'AND':
				for rule in rules:
					field = rule['field']
					op = rule['op']
					data = rule['data']
					if op == 'ne':
						s = "res = self.table.objects.exclude(%s = '%s')" %( field, data)
					elif op == 'in':
						s = "res = self.table.objects.filter(%s__in =%s)" %( field, data.split(','))
						
					elif op == 'ni':
						s = "res = self.table.objects.exclude(%s__in =%s)" %( field, data.split(','))
					else:
						s = "res = self.table.objects.filter(%s%s = '%s')" %( field, ops[op], data)
					try:
						exec(s)
					except ValidationError:
						return 'err'
			else:
				s = "res = self.table.objects.filter("
				orStr = ''
				for rule in rules:
					field = rule['field']
					op = rule['op']
					data = rule['data']
					if op == 'ne':
						s += "%s ~Q(%s = '%s') " %( orStr, field, data)
					elif op == 'in':
						s += "%s Q(%s__in = %s ) " %( orStr, field, data.split(','))
					elif op == 'ni':
						s += "%s ~Q(%s__in = %s ) " %( orStr, field, data.split(','))
					else:
						s += "%s Q(%s%s = '%s' ) " %( orStr, field, ops[op], data)
					orStr = '|'
				s += ")"
				exec(s)
			count = res.count()
			if count > 0:
				total_pages = int( math.ceil(count / float(limit) ) )
			else:
				total_pages = 0
			if page > total_pages:
				page = total_pages
			start = ( limit * page ) - limit
			if start > 0:
				start -= 1
			res = res.order_by(sidx)[abs(start):(abs(limit) + abs(start))]
		else:
			if start > 0:
				start -= 1
			res = self.table.objects.order_by(sidx)[abs(start):(abs(limit) + abs(start))]
		data = []
		try:
			for t in res:
				s = "data.append( %s )"%self.moreTemplate
				exec(s)
		except:
			s = "data.append( %s )"%self.singleTemplate
			exec(s)
		
		response = {
			'page': page, 
			'total': total_pages, 
			'rows': data,
			'records': count
			}
		return response
	
	def editHandler(self, request):
		if not self.entityErr:
			if isinstance(request, DjangoRequest):
				try:
					(operation, attrMap) = self.djangoStuff.readRequest_editHandler(request, self.AllMembers)
				except KeyError:
					return "Missing Request Object Elements"
			else:
				raise "UN-determine Request Object"
			
			if operation != 'err':
				return self._editHandler(operation, attrMap)
			return 'err' 
		else:
			return "Un-determine Entinty Class"
	'''
	operation : the operation of edit action [add, edit or del]
	attrMap   : the attributes that will be added or edited with case senstive members name of the table
	'''
	def _editHandler(self, operation, attrMap = {}):
		if operation == 'add':
			tableID = attrMap[self.tableID]
			s = "self.table.objects.get(%s = '%s')"%(self.tableID, tableID)
			try:
				try:
					if tableID == '':
						raise ObjectDoesNotExist
					exec(s)
					return 'exist'
				except ValidationError:
					return 'err'
			except ObjectDoesNotExist:
				s = "obj = self.table()"
				exec(s)
				for key in attrMap.keys():
					if key != 'id':
						t = attrMap[key]
						default = ('%s'%(self.AllMembers[key].default) != "django.db.models.fields.NOT_PROVIDED")
						auto_now = (isinstance(self.AllMembers[key], models.DateTimeField) or isinstance(self.AllMembers[key], models.DateField) or isinstance(self.AllMembers[key], models.TimeField)) and self.AllMembers[key].auto_now
						auto_now_add = (isinstance(self.AllMembers[key], models.DateTimeField) or isinstance(self.AllMembers[key], models.DateField) or isinstance(self.AllMembers[key], models.TimeField)) and self.AllMembers[key].auto_now_add
						if not(t == '' and default) or not (t == '' and auto_now)  or not (t == '' and auto_now_add):
							if isinstance(self.AllMembers[key], models.BooleanField):
								t = (t == 'True')
							s = 'obj.%s = t'%(key)
							exec(s)
				try:
					obj.save()
				except (ValidationError, ValueError):
					return 'err'
				return 'ok'
		elif operation == 'edit':
			tableID = attrMap[self.tableID]
			if tableID != '':
				try:
					s = "obj = self.table.objects.get(%s = '%s')"%(self.tableID, tableID)
					try:
						exec(s)
					except:
						return 'err'
					for key in attrMap.keys():
						if key != 'id':
							t = attrMap[key]
							default = ('%s'%(self.AllMembers[key].default) != "django.db.models.fields.NOT_PROVIDED")
							auto_now = (isinstance(self.AllMembers[key], models.DateTimeField) or isinstance(self.AllMembers[key], models.DateField) or isinstance(self.AllMembers[key], models.TimeField)) and self.AllMembers[key].auto_now
							auto_now_add = (isinstance(self.AllMembers[key], models.DateTimeField) or isinstance(self.AllMembers[key], models.DateField) or isinstance(self.AllMembers[key], models.TimeField)) and self.AllMembers[key].auto_now_add
							if not(t == '' and default) or not (t == '' and auto_now)  or not (t == '' and auto_now_add):
								if isinstance(self.AllMembers[key], models.BooleanField):
									t = (t == 'True')
								s = 'obj.%s = t'%(key)
								exec(s)
					try:
						obj.save()
					except (ValidationError, ValueError):
						return 'err'
					return 'ok'
				except:
					return 'err'
			else:
				return 'err'
		elif operation == 'del':
			ids = attrMap['id'].split(',')
			for id in ids:
				s = "res = self.table.objects.filter( %s = '%s')"%(self.tableID, id)
				exec(s)
				res.delete()
			return 'ok'
	
	'''
	rowList     : determine the options of how many rows that will be displayed in the grid
	displayList : the list of attribute that will be displayed in the grid
	rejectList  : the list of attribute that will not be displayed in the grid
	multiSelect : determine the selection options, [single row or multible rows]
	'''
	def javaScript(self, request, rowList = [5, 10, 15], displayList = [], rejectList = [], multiSelect = 'false', width = 900, height = 600, cols_width = []):
		if not self.entityErr:
			if isinstance(request, DjangoRequest):
				try:
					(htmlTableGrid, htmlDivPager, handlerURL, editURL, gridCaption) = self.djangoStuff.readRequest_javaScript(request)
				except KeyError:
					return "Missing Request Object Elements"
			else:
				raise "UN-determine Request Object"
			if not displayList:
				displayList = self.displayMembers
			return self._javaScript(htmlTableGrid, htmlDivPager, handlerURL, editURL, gridCaption, rowList, displayList, rejectList, multiSelect, width, height, cols_width)
		else:
			return "Un-determine Entinty Class"
	'''
	htmlTableGrid   : the id of the table that will contains the grid
	htmlDivPager    : the id of the div that will contains the navigator
	handlerURL      : the url of handler
	editURL         : the url of edit handler
	gridCaption     : the grid Caption
	'''
	def _javaScript(self, htmlTableGrid, htmlDivPager, handlerURL, editURL, gridCaption, rowList, displayList, rejectList, multiSelect, width, height, cols_width):

		js = '''
		<script type= 'text/javascript'>
		$(function() {
		$('#%s').jqGrid({
		url:'%s',
		datatype: 'json',
		mtype: 'GET',
		postData:{	'custom_search'	:	function(){ 
												return 'true'; 
												},
				 	'custom_filter'	:	function (){ 
				 								return '{"groupOp":"AND","rules":[{"field":"nadwa_name","op":"eq","data":"' + nadwaName + '"}]}'; 
			 									},
			 	},
		colNames:%s,
		colModel:[  ''' %(htmlTableGrid, handlerURL, self.displayMembers)
		for mem in self.displayMembers:
			col_width = 50
			if len(cols_width) > 0:
				col_width = cols_width[0]
				cols_width = cols_width[1:len(cols_width)]
			default = ''
			#if ('%s'%(self.AllMembers[mem].default) != "django.db.models.fields.NOT_PROVIDED"):
				#default = ", editrules:{defaultValue:'%s'}" % (self.AllMembers[mem].default)
				#default = ", defval:'%s'" % (self.AllMembers[mem].default)
			hidden = ''
			formatOption = ''
			choices = ''
			editType = ''
			editable = ''
			helpText = ''
			if self.AllMembers[mem].help_text:
				helpText = ", formoptions:{elmprefix:'%s'}"%self.AllMembers[mem].help_text
			auto_now = (isinstance(self.AllMembers[mem], models.DateTimeField) or isinstance(self.AllMembers[mem], models.DateField) or isinstance(self.AllMembers[mem], models.TimeField)) and self.AllMembers[mem].auto_now
			auto_now_add = (isinstance(self.AllMembers[mem], models.DateTimeField) or isinstance(self.AllMembers[mem], models.DateField) or isinstance(self.AllMembers[mem], models.TimeField)) and self.AllMembers[mem].auto_now_add
			if (self.AllMembers[mem].editable or auto_now or auto_now_add):
				editable = ', editable:true'
			if len(self.AllMembers[mem].choices) > 0:
				editType = ",edittype:'select'"
				choices = ',value:{'
				chList = []
				for list in self.AllMembers[mem].choices:
					chList.append("'%s':'%s'"%(list[0], list[1]))
				chList = ','.join(chList)
				choices += '%s}' %chList
			if isinstance(self.AllMembers[mem], models.BooleanField):
				editType = ",edittype:'select'"
				choices = ",value:{'True':'true', 'False':'false'}"
			if (len(displayList) > 0 and mem not in displayList) or (len(rejectList) > 0 and mem in rejectList):
				hidden = ',hidden:true'
			if isinstance(self.AllMembers[mem], models.DateTimeField) and helpText == '':
				formatOption = ", formoptions:{elmprefix:'e.g. [YYYY-MM-DD HH:MM:SS]'}"
			elif isinstance(self.AllMembers[mem], models.DateField) and helpText == '':
				formatOption = ", formoptions:{elmprefix:'e.g. [YYYY-MM-DD]'}"
			elif isinstance(self.AllMembers[mem], models.TimeField) and helpText == '':
				formatOption = ", formoptions:{elmprefix:'e.g. [HH:MM:SS]'}"
			
			js += "{name:'%s',index:'%s', width: %s %s %s, editoptions:{size:25 %s}, searchoptions: { sopt: ['eq', 'ne', 'in', 'lt', 'le', 'gt', 'ge']} %s %s %s %s},"%(mem, mem, col_width, editable, editType, choices, hidden, formatOption, default, helpText)
		js += ''' ],
		rowNum:%s,
		rowList:%s,
		pager: '#%s',
		sortname: '%s',
		sortorder: 'asc',
		viewrecords: true,
		multiselect: %s,
		caption:'%s',
		editurl:'%s',
		width:%s,
		height:%s,
		autowidth:true,
		forceFit:true
		});
		
		$('#%s').jqGrid('navGrid','#%s',
		{edit:true,add:true,del:true}, 
		
		{reloadAfterSubmit:true, afterSubmit : function(response, postdata) {
		if(response.responseText == 'err'){ return [false,'There is something wrong in the entered data...',-1]; }
		else if(response.responseText == 'exist'){return [false,'Record Key is allready exist!',-1]; }
		else { return [true,'',response.responseText]; }
		}, beforeShowForm : function(formid) {
			
		}
		},
		
		{reloadAfterSubmit:true, afterSubmit : function(response, postdata) { 
		if(response.responseText == 'err'){ return [false,'There is something wrong in the entered data...',-1]; }
		else if(response.responseText == 'exist'){return [false,'Record Key is allready exist!',-1]; }
		else { return [true,'',response.responseText]; }
		}
		},
		
		{reloadAfterSubmit:true}, 
		{closeOnEscape: true, multipleSearch: true, closeAfterSearch: true}
		);
		});
		</script> ''' %(rowList[0], rowList, htmlDivPager, displayList[0], multiSelect, gridCaption, editURL, width, height, htmlTableGrid, htmlDivPager)
		
		return js
		
	def buildTemplate(self, displayList):
		'''
		Reorganize order of fields as in Display List
		'''
		tempMem = [self.tableID]
		if displayList:
			for mem in displayList:
				if(mem in self.displayMembers):
					tempMem.append(mem)
			for mem in self.displayMembers:
				if(mem not in tempMem):
					tempMem.append(mem)
			self.displayMembers = tempMem
		
		self.moreTemplate = "{'id': unicode(t.%s), 'cell':(unicode(t.%s) "%(self.tableID, self.tableID)
		self.singleTemplate = "{'id': unicode(res.%s), 'cell':(unicode(res.%s) "%(self.tableID, self.tableID)
		for m in self.displayMembers:
			if m != self.tableID:
				self.moreTemplate += ', unicode(t.%s)'%m
				self.singleTemplate += ', unicode(res.%s)'%m
		self.moreTemplate += ')}'
		self.singleTemplate += ')}'