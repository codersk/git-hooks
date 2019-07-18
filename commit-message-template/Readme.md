
# How to use Git message template

If you’re not sure whether you’re already using a **Git template** in your project, try running `git config --get commit.template` in your terminal.

If no value is returned then you’re good to go.

## Check existing commit template
  git config --get commit.template  


## Create new commit template
While creating the template file in your project. Keep in mind that Git will pre-populate the editor you’ve configured for your commit messages (see Git’s [core.editor](https://git-scm.com/docs/git-config#git-config-coreeditor)  setting, which defaults to Vim) with the contents of this template. That content is what committers will see when prompted for the commit message at commit time.

## Path and name
The path and name of your template are up to you, as long as you link the `commit.template` value to the correct file. Some people prefer `.gitmessage` for the name of the file, but you can use anything ranging from `.git-message-template` to `gitmessage.txt` will work.

## Configuration
Once you have the template in place, you’ll need to configure Git to use it

`git config --local commit.template "path_to_template_file/filename"`

and _that's it_! You’re ready to `git commit` with style and format which you just have defined.

---
## _Thank you!_
_Sandeep_
---