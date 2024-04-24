import os
import tarfile
import logging
import datetime
from django.http import FileResponse
from django.conf import settings
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy

from .forms import PostForm
from .models import Post

logger = logging.getLogger(__name__)

# Create your views here.
class HomePageView(ListView):
    model = Post
    template_name = "home.html"

class CreatePostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = "post.html"
    success_url = reverse_lazy("home")

def backup_view(req):
    logger.info("Backup requested")

    # Generate a timestamp
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime('%Y%m%d-%H%M')

    # Define the directory to backup and output filename
    backup_dir = settings.MEDIA_ROOT
    output_filename = os.path.join(backup_dir, f'{timestamp}-backup.tar.gz')

    # Create the .tar.gz file
    with tarfile.open(output_filename, "w:gz") as tar:
        for item in os.listdir(settings.MEDIA_ROOT):
            if item != "lost+found":  # Exclude lost+found directory
                full_path = os.path.join(settings.MEDIA_ROOT, item)
                tar.add(full_path, arcname=os.path.basename(full_path))

    # Calculate file size in GB
    file_size = os.path.getsize(output_filename) / (1024 * 1024 * 1024)

    logger.info(f"Backup file created: {output_filename}, {file_size:.2f} GB")

    # Return the file to the requester
    try:
        response = FileResponse(open(output_filename, 'rb'), as_attachment=True, filename=os.path.basename(output_filename))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_filename)}"'
        logger.info("Backup completed successfully")
        return response
    finally:
        # Clean up: delete the file after sending it
        os.remove(output_filename)
        logger.info(f"Backup file deleted: {output_filename}")