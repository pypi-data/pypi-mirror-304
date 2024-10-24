import { launchPos } from '.';
import { createDiv, createEl } from './globals';
import { copilotParams } from './params';
import getTheme from './theme';

export const showErorrView = (title: string) => {
  const container = document.getElementById('gpt-tab')!;

  const errorViewContainer = createDiv(container);
  errorViewContainer.classList.add(
    'flex',
    'flex-col',
    'w-full',
    'h-full',
    'py-10',
    'px-4',
    'text-center',
    'text-[var(--pieces-text-muted)]',
    'justify-center'
  );
  errorViewContainer.id = 'copilot-error-view';

  const darkMode = getTheme().darkMode;

  const imgDiv = createDiv(errorViewContainer);
  imgDiv.classList.add('flex', 'justify-center');
  const img = createEl(imgDiv, 'div');
  img.classList.add(
    darkMode ? 'guy-asleep-dm' : 'guy-asleep-lm',
    'h-32',
    'w-32',
    'bg-contain',
    'bg-no-repeat'
  );

  const loadTxtContainer = createDiv(errorViewContainer);
  loadTxtContainer.classList.add('px-2', 'text-lg', 'font-bold');

  const loadTxtP = createEl(loadTxtContainer, 'p');
  loadTxtP.classList.add('m-0');
  loadTxtP.innerText = title;

  const expText = createDiv(errorViewContainer);
  expText.classList.add('pt-4', 'px-2', 'font-semibold', 'break-words');
  expText.innerHTML =
    'Please make sure that Pieces OS is running, and up to date to use the Pieces Copilot! If the issue persists, please ';

  const contactSupportBtn = createEl(expText, 'a');
  contactSupportBtn.classList.add('underline', 'cursor-pointer');
  contactSupportBtn.onclick = () => {
    copilotParams.openLink(
      'https://getpieces.typeform.com/to/mCjBSIjF#page=vscode-plugin'
    );
  };
  contactSupportBtn.innerText = 'contact support';

  const launchBtnDiv = createDiv(errorViewContainer);
  launchBtnDiv.classList.add(
    'pt-4',
    'flex-row',
    'gap-2',
    'flex',
    'justify-center'
  );

  const launchBtn = createEl(launchBtnDiv, 'button');
  launchBtn.classList.add(
    `vs-btn-${darkMode ? 'dark' : 'light'}`,
    'p-2',
    'rounded',
    'vs-btn',
    'shadow-sm',
    'shadow-[var(--pieces-background-modifier-box-shadow)]',
    'w-fit'
  );
  launchBtn.innerText = 'Launch';
  launchBtn.onclick = () => {
    launchPos();
  };

  const installBtn = createEl(launchBtnDiv, 'button');
  installBtn.classList.add(
    `vs-btn-${darkMode ? 'dark' : 'light'}`,
    'p-2',
    'rounded',
    'vs-btn',
    'shadow-sm',
    'shadow-[var(--pieces-background-modifier-box-shadow)]',
    'w-fit'
  );
  installBtn.innerText = 'Install';
  installBtn.onclick = () => {
    window.open(
      'https://docs.pieces.app/installation-getting-started/what-am-i-installing'
    );
  };
};
