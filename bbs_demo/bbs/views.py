from django.shortcuts import render, redirect
from bbs.models import Plate, Article, Comment
from bbs.forms import ArticleForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    """bbs主页"""
    plates = Plate.objects.all()
    context = {'plates': plates}
    return render(request, 'bbs/index.html', context)


def plate(request, plate_id, page):
    """板块页面"""
    plate = Plate.objects.get(id=plate_id)
    articles = plate.article_set.order_by('-date_added')

    page_size = 20    # 每页显示的帖子条目数量
    length = len(articles)
    page_num = length / page_size
    if page_num != int(page_num):
        page_num += 1
    page_num = int(page_num)
    # 分页器
    temp = int(page / 10)
    page_group = 10    # 单页显示的页码数量
    if page_num < page_group:
        page_range = range(1, page_num+1)
    if page <= page_num:
        if not page % page_group:
            start_page = (temp - 1) * page_group + 1
            page_range = range(start_page, page+1)
        else:
            if (temp + 1) * page_group < page_num:
                start_page = temp * page_group + 1
                end_page = (temp + 1) * page_group
                page_range = range(start_page, end_page+1)
            else:
                start_page = temp * page_group + 1
                page_range = range(start_page, page_num+1)
    else:
        page = page_num
        if page_num % page_group:
            start_page = int(page_num/page_group) * page_group + 1
            page_range = range(start_page, page_num+1)
        else:
            page_range = range(page_num-page_group+1, page_num+1)
    # 翻页器
    if page != 1:
        previous_page = page - 1
    else:
        previous_page = page
    if page != page_num:
        next_page = page + 1
    else:
        next_page = page

    if articles:
        start = (page - 1) * page_size
        end = page * page_size
        data = articles[start:end]
        articles = data

    context = {
        'plate': plate,
        'articles': articles,
        'present_page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'page_range': page_range,
    }
    return render(request, 'bbs/plate.html', context)


def article(request, article_id, page):
    """帖子详情页"""
    article = Article.objects.get(id=article_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article_id = article_id
            new_comment.owner_id = request.user.id
            new_comment.save()
            return redirect('bbs:article', article_id=article_id)
    comments = article.comment_set.order_by('date_added')

    page_size = 20    # 每页显示的帖子条目数量
    length = len(comments) + 1
    page_num = length / page_size
    if page_num != int(page_num):
        page_num += 1
    page_num = int(page_num)
    # 分页器
    temp = int(page / 10)
    page_group = 10  # 单页显示的页码数量
    if page_num < page_group:
        page_range = range(1, page_num + 1)
    if page <= page_num:
        if not page % page_group:
            start_page = (temp - 1) * page_group + 1
            page_range = range(start_page, page + 1)
        else:
            if (temp + 1) * page_group < page_num:
                start_page = temp * page_group + 1
                end_page = (temp + 1) * page_group
                page_range = range(start_page, end_page + 1)
            else:
                start_page = temp * page_group + 1
                page_range = range(start_page, page_num + 1)
    else:
        page = page_num
        if page_num % page_group:
            start_page = int(page_num / page_group) * page_group + 1
            page_range = range(start_page, page_num + 1)
        else:
            page_range = range(page_num - page_group + 1, page_num + 1)
    # 翻页器
    if page != 1:
        previous_page = page - 1
    else:
        previous_page = page
    if page != page_num:
        next_page = page + 1
    else:
        next_page = page

    if comments:
        # 帖子一楼占一栏, 故第 1 页显示回复的数量减 1
        if page == 1:
            start = 0
            end = page * page_size - 1
        # 后续页需整体向前 1 位, 保证每页回复数量一致
        else:
            start = (page - 1) * page_size - 1
            end = page * page_size - 1
        data = comments[start:end]
        comments = data

    context = {
        'article': article,
        'comments': comments,
        'present_page': page,
        'previous_page': previous_page,
        'next_page': next_page,
        'page_range': page_range,
    }
    return render(request, 'bbs/article.html', context)


@login_required
def post(request, plate_id):
    """发帖页面"""
    plate = Plate.objects.get(id=plate_id)

    if request.method != 'POST':
        form = ArticleForm()
    else:
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.plate_id = plate_id
            new_article.owner_id = request.user.id
            new_article.save()
            return redirect('bbs:plate', plate_id=plate.id, page=1)

    context = {'plate': plate, 'form': form}
    return render(request, 'bbs/post.html', context)


@login_required
def reply(request, article_id):
    """回复页面"""
    article = Article.objects.get(id=article_id)

    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article_id = article_id
            new_comment.owner_id = request.user.id
            new_comment.save()
            return redirect('bbs:article', article_id=article_id)

    context = {'article': article, 'form': form}
    return render(request, 'bbs/reply.html', context)


@login_required
def edit_article(request, article_id):
    """编辑帖子页面"""
    article = Article.objects.get(id=article_id)
    if article.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = ArticleForm(instance=article)
    else:
        form = ArticleForm(instance=article, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bbs:user')

    context = {'article': article, 'form': form}
    return render(request, 'bbs/edit_article.html', context)


@login_required
def edit_comment(request, comment_id):
    """编辑回复页面"""
    comment = Comment.objects.get(id=comment_id)
    if comment.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bbs:user')

    context = {'comment': comment, 'form': form}
    return render(request, 'bbs/edit_comment.html', context)


@login_required
def delete_article(request, article_id):
    """删除帖子页面"""
    article = Article.objects.get(id=article_id)
    if article.owner != request.user:
        raise Http404
    article.delete()
    return redirect('bbs:my_article')


@login_required
def delete_comment(request, comment_id):
    """删除回复页面"""
    comment = Comment.objects.get(id=comment_id)
    if comment.owner != request.user:
        raise Http404
    comment.delete()
    return redirect('bbs:my_comment')


@login_required
def my_article(request):
    """用户发帖记录页面"""
    articles = Article.objects.filter(owner=request.user).order_by('-date_added')
    context = {'articles': articles}
    return render(request, 'bbs/my_article.html', context)


@login_required
def my_comment(request):
    """用户回复记录页面"""
    comments = Comment.objects.filter(owner=request.user).order_by('-date_added')
    context = {'comments': comments}
    return render(request, 'bbs/my_comment.html', context)
