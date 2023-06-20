import flet as ft
from pytube import YouTube
import os

file_data = ""


def main(page: ft.Page):
    page.title = "Youtube Downloader"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def download_file(e: ft.FilePickerResultEvent):
        global file_data
        directory_path = e.path if e.path else "Cancelled!"
        if directory_path != "Cancelled!":
            p_download.visible = True
            status_download.value = "Downloading..."
            p_download.update()
            status_download.update()
            if file_data.resolution:  # dowload video
                file_data.download(output_path=str(directory_path))
            else:  # dowload audio
                out_file = file_data.download(output_path=str(directory_path))
                base = list(os.path.splitext(out_file))
                new_file = base[0] + ".mp3"
                os.rename(out_file, new_file)

            status_download.value = "Download complete!"
            p_download.visible = False
            p_download.update()
            status_download.update()

    def btn_getlink(e):
        global file_data
        file_data = e.control.data
        status_download.value = ""
        yt_list.controls.clear()
        yt_list.controls.append(yt_title)
        yt_list.controls.append(yt_author)
        yt_list.controls.append(section_download)
        page.update()

    def go(e):
        if not search_input.value:
            search_input.error_text = "Please enter the YouTube video URL!"
            search_input.update()
        else:
            try:
                p_search.visible = True
                search_input.error_text = ""
                yt_list.controls.clear()
                search_input.update()
                p_search.update()
                yt_list.update()
                yt = YouTube(search_input.value)
                yt_title.value = yt.title
                yt_author.value = yt.author
                yt_image.src = yt.thumbnail_url
                yt_image.visible = True
                yt_list.controls.append(yt_title)
                yt_list.controls.append(yt_author)

                # Get mp4
                yt_list.controls.append(
                    ft.Text("Select MP4 video:", weight=ft.FontWeight.BOLD)
                )
                response = (
                    yt.streams.filter(progressive=True, file_extension="mp4")
                    .order_by("resolution")
                    .desc()
                )
                for i in range(0, len(response)):
                    item = ft.Row(
                        [
                            ft.Text(value=response[i].resolution),
                            ft.ElevatedButton(
                                text="Get link",
                                data=response[i],
                                on_click=btn_getlink,
                            ),
                        ]
                    )
                    yt_list.controls.append(item)

                # get audio
                yt_list.controls.append(
                    ft.Text("Select MP3 audio:", weight=ft.FontWeight.BOLD)
                )
                response_audio = (
                    yt.streams.filter(only_audio=True).order_by("abr").desc()
                )
                for i in range(0, len(response_audio)):
                    item = ft.Row(
                        [
                            ft.Text(value=response_audio[i].abr),
                            ft.ElevatedButton(
                                text="Get link",
                                data=response_audio[i],
                                on_click=btn_getlink,
                            ),
                        ]
                    )
                    yt_list.controls.append(item)
                p_search.visible = False
                p_search.update()
                page.update()

            except:
                search_input.error_text = "URL no exist!"
                search_input.update()
                p_search.visible = False
                p_search.update()

    # section title
    section_title = ft.Column(
        [
            ft.Row(
                [
                    ft.Image(
                        src="youtube-logo.jpg",
                        width=150,
                        height=150,
                        fit=ft.ImageFit.CONTAIN,
                    ),
                    ft.Text(value="Downloader", size=45),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(value="Download Youtube videos in MP4,MP3 for free"),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # section search
    search_input = ft.TextField(label="Enter the YouTube video URL: ", width=600)
    btn_go = ft.ElevatedButton(text="Go", on_click=go, height=50, width=100)
    p_search = ft.ProgressRing(visible=False)
    section_search = ft.Row(
        [search_input, btn_go, p_search],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # section result of youtube
    yt_title = ft.Text(weight=ft.FontWeight.BOLD, width=450)
    yt_author = ft.Text()
    yt_image = ft.Image(width=400, height=250, src="youtube-logo.jpg", visible=False)
    yt_list = ft.ListView(
        expand=1, spacing=15, padding=20, auto_scroll=True, height=400
    )
    section_yt = ft.Row(
        [
            yt_image,
            yt_list,
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )

    # section download
    status_download = ft.Text(value="")
    p_download = ft.ProgressRing(visible=False)
    section_download = ft.Row(
        [
            ft.ElevatedButton(
                text="download",
                icon=ft.icons.DOWNLOAD,
                on_click=lambda _: get_directory_dialog.get_directory_path(),
            ),
            status_download,
            p_download,
        ]
    )

    # Dialog directory
    get_directory_dialog = ft.FilePicker(on_result=download_file)
    page.overlay.append(get_directory_dialog)

    page.add(ft.Column([section_title, section_search, section_yt]))


if __name__ == "__main__":
    ft.app(target=main)
