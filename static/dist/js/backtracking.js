const commands = []
const input = document.querySelector('input')

function saveCommand(e) {
  commands.push({

    action: { type: 'add', key: e.key, index: input.selectionStart },
    inverse: { type: 'remove', index: input.selectionStart }
  })
}

function undo() {
  let value = input.value.split('')
  const lastCommand = commands.pop()
 
  if (!lastCommand) return

  switch (lastCommand.inverse.type) {
    case 'remove':
      value.splice(lastCommand.inverse.index, 1)
      break;
  }

  input.value = value.join('')
}