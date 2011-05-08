# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ImageType'
        db.create_table('fusion_imagetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('typename', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('infourl', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('dataurl', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('longdescription', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('sourcesystemid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('canbethen', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hide', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('fusion', ['ImageType'])

        # Adding model 'Image'
        db.create_table('fusion_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fusion.ImageType'])),
            ('imageurl', self.gf('django.db.models.fields.URLField')(unique=True, max_length=256)),
            ('thumburl', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('infourl', self.gf('django.db.models.fields.URLField')(max_length=256, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('sourcesystemid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('creator', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('dateofwork', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('hide', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('fusion', ['Image'])

        # Adding model 'Fusion'
        db.create_table('fusion_fusion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('then', self.gf('django.db.models.fields.related.ForeignKey')(related_name='then', to=orm['fusion.Image'])),
            ('now', self.gf('django.db.models.fields.related.ForeignKey')(related_name='now', to=orm['fusion.Image'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('points', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=512)),
            ('cropthen', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=20)),
            ('publish', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('hide', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('flagged', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('fusion', ['Fusion'])


    def backwards(self, orm):
        
        # Deleting model 'ImageType'
        db.delete_table('fusion_imagetype')

        # Deleting model 'Image'
        db.delete_table('fusion_image')

        # Deleting model 'Fusion'
        db.delete_table('fusion_fusion')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'fusion.fusion': {
            'Meta': {'object_name': 'Fusion'},
            'cropthen': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '20'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'flagged': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'now': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'now'", 'to': "orm['fusion.Image']"}),
            'points': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '512'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'then': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'then'", 'to': "orm['fusion.Image']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'fusion.image': {
            'Meta': {'object_name': 'Image'},
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'dateofwork': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'hide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imageurl': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '256'}),
            'infourl': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'sourcesystemid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'thumburl': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fusion.ImageType']"})
        },
        'fusion.imagetype': {
            'Meta': {'object_name': 'ImageType'},
            'canbethen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dataurl': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'hide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infourl': ('django.db.models.fields.URLField', [], {'max_length': '256', 'blank': 'True'}),
            'longdescription': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'sourcesystemid': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'typename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        }
    }

    complete_apps = ['fusion']
