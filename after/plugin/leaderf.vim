" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "vista",
            \   "help": "navigate the vista outline",
            \   "manager_id": "leaderf#Vista#managerId",
            \   "arguments": [
            \   ]
            \ }
" In order that `Leaderf marks` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=0 LeaderfVista Leaderf vista

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfVista", "navigate the vista outline")