import sublime, sublime_plugin
import os, re, textwrap
# alt+super+8

try:
  from .Edit import Edit as Edit
except:
  from Edit import Edit as Edit

class ViewToPartialCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    self.edit = edit
    self.view.window().show_input_panel("Partial name:", "", self.get_selected_text, None, None)

  def get_selected_text(self, partial_name):
    region = self.view.sel()[0]

    # lines = self.view.lines(region)
    # print(lines) # [(83, 100), (101, 124), (125, 125), (126, 166), (167, 284)]

    # line  = self.view.line(region)
    # print(line) # (83, 284)

    # lines = self.view.substr(region).split('\n')
    # print(lines)
    # for i in lines:
    #   print(i)

    if not region.empty():
      partial_code = self.view.substr(region)
      self.create_partial_file(partial_name, partial_code)

  def create_partial_file(self, partial_name, partial_code):
    source                      = self.view.file_name()
    source_path                 = os.path.dirname(source)
    rails_view_path             = os.path.dirname(source_path)
    original_file_extension     = self.view.file_name().split('.')[1]

    if original_file_extension == 'html':
      partial_name_with_extension = partial_name + '.' + original_file_extension + '.erb'
    else:
      partial_name_with_extension = partial_name + '.' + original_file_extension

    partial_file_with_path      = source_path + '/_' + partial_name_with_extension

    new_class_code = partial_code

    if not os.path.exists(partial_file_with_path):
      with open(partial_file_with_path, 'w') as f:
        f.write(textwrap.dedent(new_class_code))

    self.insert_class_reference(partial_name, original_file_extension)

    self.view.window().open_file(partial_file_with_path)

  def insert_class_reference(self, partial_name, original_file_extension):
    region = self.view.sel()[0]

    # TODO correctly calculate spaces before new_region

    if original_file_extension == 'html':
      new_region = "<%= render '" + partial_name + "' %>"
    else:
      new_region = "= render '" + partial_name + "'"

    with Edit(self.view) as edit:
      edit.replace(region, new_region)