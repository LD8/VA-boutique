from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Item, SubCategory, IndexCarousel
# Q helps to search A or B at the same time
from django.db.models import Q


class IndexView(ListView):
    '''landing page'''
    model = Category
    template_name = 'boutique/index.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['carousels'] = IndexCarousel.objects.all()
        return context


class CategoryListView(ListView):
    '''display a list of items'''
    model = Category
    paginate_by = 1
    template_name = 'boutique/items.html'
    # context_object_name is actually the result of `get_queryset()`
    context_object_name = 'category_shown'

    def get_queryset(self):
        # get original queryset: Category.objects.all()
        qs = super().get_queryset()

        # filter men/women
        if self.kwargs.get('gender') == 'Women':
            qs = qs.filter(gender=1)
        elif self.kwargs['gender'] == 'Men':
            qs = qs.filter(gender=2)

        if self.kwargs.get('category_pk'):
            qs = qs.filter(pk=self.kwargs.get('category_pk'))

        # print('\nqs= ', qs, '\n')
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add categories for navbar link texts
        context['categories'] = Category.objects.all()

        if self.kwargs.get('subcategory_pk'):
            context['subcategory_shown'] = get_object_or_404(
                SubCategory, pk=self.kwargs.get('subcategory_pk'))
            context['item_list'] = Item.objects.filter(
                subcategory=self.kwargs.get('subcategory_pk'))
            # print('\ncontext with subcat= ', context, '\n')
            return context

        # Because context_object_name actually represents the result of `get_queryset()`
        # Therefore, if context_object_name is set to the same name as the context name
        # the following expression can be omitted
        # context['category_shown'] = self.get_queryset()
        # The benefit of this is you don't need to run get_queryset() again!!

        if self.kwargs.get('category_pk'):
            context['item_list'] = Item.objects.filter(
                category=self.kwargs.get('category_pk'))

        # print('\ncontext= ', context, '\n')
        return context


class ItemDetailView(DetailView):
    '''display an individual item'''
    model = Item
    template_name = 'boutique/item.html'
    # no need to specify as default context_object_name depends on the model
    # they are actually the same (with lower case first letter)
    # context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # add categories for navbar link texts
        context['categories'] = Category.objects.all()
        # print('\ncontext= ', context, '\n')
        return context


class SearchView(ListView):
    model = Category
    template_name = 'boutique/search.html'
    context_object_name = 'items'

    def get_queryset(self):
        query = self.kwargs['query']
        items = Item.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(subcategory__icontains=query) |
            Q(description__icontains=query))

        return items
    
    def get(self, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['search_result'] = self.get_queryset()
        print(context)
        return context



# def search(request, query=None, topic_pk=None):
#     # if no-input submission --> redirect to topics for users to browse
#     if request.GET.get('query') == '':
#         return redirect('forum:topics')

#     # if user searching from nav bar, get the request query value stored properly
#     if query == None:
#         query = request.GET.get('query')

#     # search through all Post objects, in titles and contents
#     search_result_posts = Post.objects.filter(
#         Q(title__icontains=query) |
#         Q(content__icontains=query) |
#         Q(date_added__icontains=query))

#     # because there are only a few topics,
#     # use filtered posts to determine topics for displaying in the sidebar
#     search_result_topics = []
#     for post in search_result_posts:
#         if post.topic not in search_result_topics:
#             search_result_topics.append(post.topic)

#     # passing an empty topic if topic_pk=None
#     search_result_topic = {}

#     # if to check results in a specific topic
#     if topic_pk != None:
#         # make sure this topic exists and override the default value
#         search_result_topic = get_object_or_404(Topic, pk=topic_pk)
#         # search through all the posts in this topic, and override previous search_results_posts
#         search_result_posts = search_result_topic.post_set.filter(
#             Q(title__icontains=query) |
#             Q(content__icontains=query))

#     return render(request, 'forum/search.html', {
#         'search_result_posts': search_result_posts,
#         'search_result_topics': search_result_topics,
#         'search_result_topic': search_result_topic,
#         'query': query})
