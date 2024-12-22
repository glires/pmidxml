#!/usr/bin/env python

'''
pmidxml.py - extract citation information from PubMed XML data
usage: import pmidxml
'''

__author__ = 'Kohji OKAMURA, Ph.D.'
__version__ = 0.1
__date__    = '2024-09-22'
__version__ = 0.2
__date__    = '2024-09-29'
__version__ = 0.3
__date__    = '2024-12-22'

import re
import sys

months = { '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun',
           '07': 'Jul', '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec' }
flag_doi = 0

def get_title(root):
  for value in root.iter('ArticleTitle'):
    re_fullmatch = re.fullmatch(r'(.+)\.', value.text)
    if re_fullmatch: return re_fullmatch.group(1)
    else:            return value.text

def get_authors(root):
  names, initials = [], []
  for value in root.iter('LastName'): names.append(value.text)
  for value in root.iter('Initials'): initials.append(value.text)
  if len(names) != len(initials):
    sys.stderr.write('Error: Number of authors cannot be determined.\n')
    sys.exit(21)
  authors = ''
  for i in range(len(names)):
    if i > 0: authors += ', '
    authors += names[i] + ' ' + initials[i]
  return authors

def get_journal(root):
  terms = {'Genome', 'DNA', 'Cell', 'Stem', 'Cancer', 'Methods', 'Blood',
      'Genes', 'Epigenetics', 'Development', 'Nucleic', 'Acids', 'EMBO',
      'PLOS', 'ONE', 'Nature', 'Science', 'Minerva'}
  journal = ''
  for value in root.iter('ISOAbbreviation'):
    name = value.text.split(' ')
    for word in name:
      if journal != '': journal += ' '
      if word in terms: journal += word
      else:             journal += word + '.'
  return journal

def get_volume(root):
  global flag_doi
  for value in root.iter('JournalIssue'):
    if value.find('Volume') is None:
      for value in root.findall('.//ArticleId[@IdType="doi"]'):
        flag_doi = 1
        return value.text
    else:
      flag_doi = 0
      return value.find('Volume').text

def get_issue(root):
  for value in root.iter('JournalIssue'):
    if value.find('Issue') is None: return ''
    else: return '(' + value.find('Issue').text + ')'

def get_pages(root):
  start, end = '', ''
  for value in root.iter('StartPage'): start = value.text
  for value in root.iter('EndPage'): end = value.text
  if end == '': return start
  else: return start + '-' + end

def get_year(root):
  for value in root.iter('PubDate'): return value.find('Year').text

def get_month(root):
  for value in root.iter('PubDate'):
    if value.find('Month') is None:
      for value in root.iter('ArticleDate'): return months[value.find('Month').text]
    return value.find('Month').text
