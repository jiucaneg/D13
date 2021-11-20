from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from .models import Post, User, Shot, Response
from .forms import ResponseForm, PostForm, ImageForm
from django.forms import modelformset_factory
from .filters import PostFilter
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def email_notification(template, context, subject, body, email):
    html_content = render_to_string(
        template,
        context,

    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=f'{settings.DEFAULT_FROM_EMAIL}',
        to=[email, ],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


def main_redirect(request):
    response = redirect('/')
    return response


def agree(request, response_id):
    response = Response.objects.get(pk=response_id)
    response.status = True
    response.save()
    # notification to Response author
    email_notification(
        template='desk/agree_response.html',
        context={
            'response': response,
            'user': request.user,
        },
        subject=f'{request.user} принял отклик на <<{response.post.title}>>',
        body='',
        email=request.user.email
    )

    page = redirect('/filter/')
    return page


def disagree(request, response_id):
    response = Response.objects.get(pk=response_id)
    response.status = False
    response.save()
    page = redirect('/filter/')
    return page


class PostList(ListView):
    model = Post
    template_name = 'desk/post_list.html'
    context_object_name = 'post_list'


class PostDetail(FormMixin, DetailView):
    model = Post
    template_name = 'desk/post_detail.html'
    form_class = ResponseForm
    context_object_name = 'post_detail'

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = ResponseForm(initial={'post': self.object, 'author': self.request.user})
        return context

    def form_valid(self, form):
        form.save()
        return super(PostDetail, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():

            # notification to Post author
            email_notification(
                template='desk/post_author_notification.html',
                context={
                    'object': self.object,
                    'user': self.request.user,
                },
                subject=f'Отклик на {self.object.title} от {self.request.user}',
                body='',
                email=self.object.author.email
            )

            # notification to Response author
            email_notification(
                template='desk/response_author_notification.html',
                context={
                    'object': self.object,
                    'user': self.request.user,
                },
                subject=f'Вы откликнулись на {self.object.title}',
                body='',
                email=self.request.user.email
            )

            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostAdd(ListView):
    model = Post
    template_name = 'desk/post_add.html'
    form_class = PostForm
    ImageFormSet = modelformset_factory(Shot, form=ImageForm, extra=3)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(initial={'author': self.request.user})
        context['formset'] = self.ImageFormSet(queryset=Shot.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        post = self.form_class(request.POST)
        formset = self.ImageFormSet(request.POST, request.FILES, )

        if post.is_valid() and formset.is_valid():
            new_post = post.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Shot.objects.create(post=new_post, image=image)

            return redirect(new_post)


class UserDetail(DetailView):
    model = User
    template_name = 'desk/user_detail.html'
    context_object_name = 'user_detail'


class UserPrivatePage(ListView):
    model = Post
    template_name = 'desk/post_filter.html'
    context_object_name = 'post_list'
    paginate_by = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context
