from django.db import models

# Create your models here.
class User(models.Model):
    num=models.CharField(max_length=64,verbose_name='编号',unique=True,null=True)
    username=models.CharField(max_length=64,verbose_name='用户名')
    password=models.CharField(max_length=64,verbose_name='密码')
    # cho=(("1",'回答者'))
    # shenfen =models.CharField(max_length=64,choices=cho,verbose_name='身份',)
    class Meta:
        verbose_name_plural = '用户表'

class Keguan(models.Model):
    question_content=models.CharField(max_length=64,verbose_name='题目内容')
    cho=(("A",'A'),("B",'B'),("C",'C'),("D",'D'))
    bingo_answer=models.CharField(choices=cho,max_length=64,verbose_name='这道题正确的选项')
    val=models.CharField(max_length=64,verbose_name='分值')
    class Meta:
        verbose_name_plural = '客观题库'
    def __str__(self):
        return '题目:%s'%(self.question_content)
class Choise_keguan(models.Model):
    choise_keguan=models.CharField(max_length=64,verbose_name='abcd选项')
    TM=models.ForeignKey(to=Keguan,verbose_name='题目id',on_delete=models.CASCADE)
    choise_answer=models.CharField(max_length=64,verbose_name='选项的答案')
    class Meta:
        verbose_name_plural = '客观题选项表'

class Zhuguan(models.Model):
    question_content = models.CharField(max_length=64, verbose_name='题目内容')
    answer_key =models.CharField(max_length=64, verbose_name='题目的关键字')
    val = models.IntegerField(verbose_name='分值')
    class Meta:
        verbose_name_plural = '主观题库'
    def __str__(self):
        return '题目:%s'%(self.question_content)


class keguan_kaojuan(models.Model):
    student_id=models.ForeignKey(to=User,on_delete=models.CASCADE)
    tm_id=models.ForeignKey(to=Keguan,on_delete=models.CASCADE)
    answer = models.CharField(max_length=64, verbose_name='用户填写答案')
    val=models.IntegerField(verbose_name='分数',null=True)
    max_val = models.IntegerField(null=True, verbose_name='这题最大分数')
    class Meta:
        verbose_name_plural = '客观题的考试卷'

class zhuguan_kaojuan(models.Model):
    student_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    tm_id = models.ForeignKey(to=Zhuguan, on_delete=models.CASCADE)
    answer = models.CharField(max_length=64, verbose_name='用户填写的答案')
    val = models.IntegerField(null=True, verbose_name='分数')
    max_val = models.IntegerField(null=True, verbose_name='这题最大分数')

    class Meta:
        verbose_name_plural = '主观题的考试卷'

class Conf(models.Model):
    conf1=models.IntegerField(verbose_name='题目量')
    class Meta:
        verbose_name_plural = '配置'

