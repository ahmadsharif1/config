" F2 saves.
map <F2> :w! <CR>
map! <F2> <ESC>:w! <CR>

noremap <Space> <PageDown>
noremap <S-Space> <PageUp>

map <C-l> :tabnext<CR>
map <C-h> :tabprevious<CR>
map , :A<CR>

set hlsearch
set number
set incsearch

set ic
set backupdir=$HOME/backup/
set lbr
" Convert tabs to 2 spaces exactly
"""set tabstop=2
set et
set sw=2

map <C-w> :call MyQuit()<CR>

function MyQuit()
  let l:nBuffers = bufnr('$')
  let l:currBuffer = bufnr('%')

  if &modified != 0
    echo "Attempting to close modified buffer!"
    return
  endif

  if GetNumberOfListedBuffers() >= 2
    execute ":bwipeout"
    execute "syntax on"
    "execute ":bdelete"
  else
    execute ":quit"
  endif
  return
endfunction

function GetNumberOfListedBuffers()
  " Get the number of *listed* buffers.
  let l:highbuf = bufnr("$")
  let l:numlisted = 0
  let l:i = 1
  while (l:i <= l:highbuf)
    "Skip unlisted buffers.
    if (bufexists(l:i) != 0 && buflisted(l:i))
      let l:numlisted = l:numlisted + 1
    endif
    let l:i = l:i + 1
  endwhile
  return numlisted
endfunction

