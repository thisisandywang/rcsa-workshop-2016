from haystack.utils import Highlighter
from django.utils.html import strip_tags
import datetime

class MyHighlighter(Highlighter):
    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)

        half_window_length = (end_offset - start_offset)//2
        middle_point = start_offset
        end_offset = middle_point + half_window_length
        start_offset -= half_window_length
        if middle_point < half_window_length:
            end_offset += half_window_length - middle_point
            start_offset = 0


        return self.render_html(highlight_locations, start_offset, end_offset)

def in_current_semester(date):
    now = datetime.datetime.now()
    semester = {}
    for i in range(1, 6):
        semester[i] = 'Spring'
    for i in range(8, 13):
        semester[i] = 'Fall'
    return date.year == now.year and semester[date.month] == semester[now.month]
