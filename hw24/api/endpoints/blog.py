from ninja import Router
from typing import List, Optional
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from ..models import Post, Tag, Comment
from ..schemas import PostIn, PostOut, TagIn, TagOut, CommentIn, CommentOut
from ..auth import bearer_auth

router = Router()


@router.get("/tags", response=List[TagOut], auth=bearer_auth)
def list_tags(request):
    """
    Retrieves all available blog tags.
    :param request: standard Django HTTP request object
    :return: list of Tag instances
    """
    return Tag.objects.all()


@router.post("/tags", response={201: TagOut}, auth=bearer_auth)
def create_tag(request, data: TagIn):
    """
    Creates a new blog tag.
    :param request: standard Django HTTP request object
    :param data: Pydantic schema containing tag name
    :return: tuple of HTTP status code 201 and the created Tag instance
    """
    tag = Tag.objects.create(**data.dict())
    return 201, tag


@router.get("/", response=List[PostOut], auth=bearer_auth)
def list_posts(request, tag_name: Optional[str] = None):
    """
    Retrieves all blog posts, optionally filtered by tag name.
    :param request: standard Django HTTP request object
    :param tag_name: optional tag name filter
    :return: list of formatted blog posts
    """
    posts = Post.objects.select_related(
        'author').prefetch_related('tags').all()
    if tag_name:
        posts = posts.filter(tags__name__iexact=tag_name)

    return [
        {
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "author_username": p.author.username,
            "created_at": p.created_at,
            "tags": p.tags.all()
        } for p in posts
    ]


@router.get("/{post_id}", response=PostOut, auth=bearer_auth)
def get_post(request, post_id: int):
    """
    Retrieves a single blog post's details by its ID.
    :param request: standard Django HTTP request object
    :param post_id: unique integer identifier of the blog post
    :return: dictionary representing the formatted blog post
    """
    p = get_object_or_404(Post.objects.select_related(
        'author').prefetch_related('tags'), id=post_id)
    return {
        "id": p.id,
        "title": p.title,
        "content": p.content,
        "author_username": p.author.username,
        "created_at": p.created_at,
        "tags": p.tags.all()
    }


@router.post("/", response={201: PostOut}, auth=bearer_auth)
def create_post(request, data: PostIn):
    """
    Creates a new blog post written by the authenticated user.
    :param request: standard Django HTTP request object containing authenticated user
    :param data: Pydantic schema containing post title, content, and optional tag IDs
    :return: tuple of HTTP status code 201 and the formatted post dictionary
    """
    tags = Tag.objects.filter(id__in=data.tag_ids)
    post = Post.objects.create(
        title=data.title,
        content=data.content,
        author=request.user
    )
    post.tags.set(tags)
    return 201, {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_username": post.author.username,
        "created_at": post.created_at,
        "tags": post.tags.all()
    }


@router.put("/{post_id}", response=PostOut, auth=bearer_auth)
def update_post(request, post_id: int, data: PostIn):
    """
    Updates an existing blog post. The authenticated user must be the author.
    :param request: standard Django HTTP request object containing authenticated user
    :param post_id: unique integer identifier of the blog post to update
    :param data: Pydantic schema containing updated post title, content, and tag IDs
    :return: formatted post dictionary
    """
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        raise HttpError(403, "You can only edit your own posts.")

    tags = Tag.objects.filter(id__in=data.tag_ids)
    post.title = data.title
    post.content = data.content
    post.save()
    post.tags.set(tags)

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_username": post.author.username,
        "created_at": post.created_at,
        "tags": post.tags.all()
    }


@router.delete("/{post_id}", response={204: None}, auth=bearer_auth)
def delete_post(request, post_id: int):
    """
    Deletes an existing blog post. The authenticated user must be the author.
    :param request: standard Django HTTP request object containing authenticated user
    :param post_id: unique integer identifier of the post to delete
    :return: tuple of HTTP status code 204 and None
    """
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        raise HttpError(403, "You can only delete your own posts.")
    post.delete()
    return 204, None


@router.post("/{post_id}/comments", response={201: CommentOut}, auth=bearer_auth)
def add_comment(request, post_id: int, data: CommentIn):
    """
    Adds a comment to an existing blog post.
    :param request: standard Django HTTP request object containing authenticated user
    :param post_id: unique integer identifier of the post to comment on
    :param data: Pydantic schema containing comment content
    :return: tuple of HTTP status code 201 and formatted comment dictionary
    """
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(
        post=post,
        author=request.user,
        content=data.content
    )
    return 201, {
        "id": comment.id,
        "post_id": comment.post_id,
        "author_username": comment.author.username,
        "content": comment.content,
        "created_at": comment.created_at
    }


@router.get("/{post_id}/comments", response=List[CommentOut], auth=bearer_auth)
def list_comments(request, post_id: int):
    """
    Retrieves all comments associated with a specific blog post.
    :param request: standard Django HTTP request object
    :param post_id: unique integer identifier of the blog post
    :return: list of formatted comment dictionaries
    """
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post).select_related('author')
    return [
        {
            "id": c.id,
            "post_id": c.post_id,
            "author_username": c.author.username,
            "content": c.content,
            "created_at": c.created_at
        } for c in comments
    ]
