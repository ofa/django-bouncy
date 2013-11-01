# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Bounce'
        db.create_table(u'django_bouncy_bounce', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sns_topic', self.gf('django.db.models.fields.CharField')(max_length=350)),
            ('sns_messageid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mail_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('mail_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mail_from', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('feedback_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('feedback_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('hard', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('bounce_type', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('bounce_subtype', self.gf('django.db.models.fields.CharField')(max_length=50, db_index=True)),
            ('reporting_mta', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True)),
            ('diagnostic_code', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
        ))
        db.send_create_signal(u'django_bouncy', ['Bounce'])

        # Adding model 'Complaint'
        db.create_table(u'django_bouncy_complaint', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('sns_topic', self.gf('django.db.models.fields.CharField')(max_length=350)),
            ('sns_messageid', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mail_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('mail_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mail_from', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('feedback_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('feedback_timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('useragent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('feedback_type', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=150, null=True, blank=True)),
            ('arrival_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_bouncy', ['Complaint'])


    def backwards(self, orm):
        # Deleting model 'Bounce'
        db.delete_table(u'django_bouncy_bounce')

        # Deleting model 'Complaint'
        db.delete_table(u'django_bouncy_complaint')


    models = {
        u'django_bouncy.bounce': {
            'Meta': {'object_name': 'Bounce'},
            'action': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'bounce_subtype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'bounce_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'diagnostic_code': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'feedback_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'feedback_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'hard': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_from': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'mail_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reporting_mta': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sns_messageid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sns_topic': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'status': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'})
        },
        u'django_bouncy.complaint': {
            'Meta': {'object_name': 'Complaint'},
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'arrival_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feedback_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'feedback_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'feedback_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail_from': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'mail_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'mail_timestamp': ('django.db.models.fields.DateTimeField', [], {}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sns_messageid': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'sns_topic': ('django.db.models.fields.CharField', [], {'max_length': '350'}),
            'useragent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['django_bouncy']