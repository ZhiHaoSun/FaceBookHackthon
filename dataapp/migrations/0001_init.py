# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):

      # Adding model 'CompanyProfile'
        db.create_table(u'dataapp_CompanyProfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user', to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('introduction', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('detail', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'dataapp', ['CompanyProfile'])

        # Adding model 'Career'
        db.create_table(u'dataapp_Career', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='company', to=orm['dataapp.CompanyProfile'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('careerType', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'dataapp', ['Career'])

        # Adding model 'StudentRecord'
        db.create_table(u'dataapp_StudentRecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('salutation', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('matric', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('studyYear', self.gf('django.db.models.fields.IntegerField')()),
            ('CV', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'dataapp', ['StudentRecord'])

        # Adding model 'SubmissionRecord'
        db.create_table(u'dataapp_SubmissionRecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(related_name='student', to=orm['dataapp.StudentRecord'])),
            ('career', self.gf('django.db.models.fields.related.ForeignKey')(related_name='career', to=orm['dataapp.Career'])),
            ('company', self.gf('django.db.models.fields.related.ForeignKey')(related_name='company', to=orm['dataapp.CompanyProfile'])),
        ))
        db.send_create_signal(u'dataapp', ['SubmissionRecord'])

    def backwards(self, orm):
        # Deleting model 'CompanyProfile'
        db.delete_table(u'dataapp_CompanyProfile')

        # Deleting model 'Career'
        db.delete_table(u'dataapp_Career')

        # Deleting model 'StudentRecord'
        db.delete_table(u'dataapp_StudentRecord')

        # Deleting model 'SubmissionRecord'
        db.delete_table(u'dataapp_SubmissionRecord')

    models = {
        u'dataapp.career': {
            'Meta': {'object_name': 'Career'},
            'careerType': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataapp.CompanyProfile']"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'dataapp.companyprofile': {
            'Meta': {'object_name': 'CompanyProfile'},
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth_account.User']"}),
            'detail': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        u'dataapp.studentrecord': {
            'CV': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'Meta': {'object_name': 'StudentRecord'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'firstname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'major': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'matric': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'salutation': ('django.db.models.fields.CharField', [], {'default': "'Mr.'", 'max_length': '10'}),
            'school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'studyYear': ('django.db.models.fields.IntegerField', [], {})
        },
        u'dataapp.submissionrecord': {
            'Meta': {'object_name': 'SubmissionRecord'},
            'career': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataapp.Career']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataapp.StudentRecord']"}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dataapp.CompanyProfile']"})
        }
    }

    complete_apps = ['dataapp']
    symmetrical = True
