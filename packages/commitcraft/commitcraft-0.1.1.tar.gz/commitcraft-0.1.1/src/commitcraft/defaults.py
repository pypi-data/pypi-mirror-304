default={
    'commit_guidelines' : '''
    - Never ask for folow-up questions.
    - Don't ask quetions.
    - Don't talk about yourself.
    - Be concise and clear.
    - Be informative.
    - Don't explain row by row just the global goal of the changes.
    - Avoid unecessary details and long explanations.
    - Use action verbs.
    - Use bullet points in the body if there are many changes
    - Do not talk about the hashes.
    - Create concise and comprehensive commit messages.
    - Be direct about what changed and why. Focous on what.
    - Give a small summary of what has changed and how it may afect the rest of the project. 
    - Do not return any explanation other then the commit message itself.
    - If there are many changes focous on the main ones.
    - The first row shall be te title of your message, so make it simple and informative.
    
    ''',
    'emoji_guidelines' :{
        'full':'''
    For the title of your message use the GitMoji Convetion, here is some help emoji ; description:
        🎨 ; Improve structure / format of the code.
        ⚡️ ; Improve performance.
        🔥 ; Remove code or files.
        🐛 ; Fix a bug.
        🚑️ ; Critical hotfix.
        ✨ ; Introduce new features.
        📝 ; Add or update documentation.
        🚀 ; Deploy stuff.
        💄 ; Add or update the UI and style files.
        🎉 ; Begin a project.
        ✅ ; Add, update, or pass tests.
        🔒️ ; Fix security or privacy issues.
        🔐 ; Add or update secrets.
        🔖 ; Release / Version tags.
        🚨 ; Fix compiler / linter warnings.
        🚧 ; Work in progress.
        💚 ; Fix CI Build.
        ⬇️ ; Downgrade dependencies.
        ⬆️ ; Upgrade dependencies.
        📌 ; Pin dependencies to specific versions.
        👷 ; Add or update CI build system.
        📈 ; Add or update analytics or track code.
        ♻️ ; Refactor code.
        ➕ ; Add a dependency.
        ➖ ; Remove a dependency.
        🔧 ; Add or update configuration files.
        🔨 ; Add or update development scripts.
        🌐 ; Internationalization and localization.
        ✏️ ; Fix typos.
        💩 ; Write bad code that needs to be improved.
        ⏪️ ; Revert changes.
        🔀 ; Merge branches.
        📦️ ; Add or update compiled files or packages.
        👽️ ; Update code due to external API changes.
        🚚 ; Move or rename resources (e.g.: files, paths, routes).
        📄 ; Add or update license.
        💥 ; Introduce breaking changes.
        🍱 ; Add or update assets.
        ♿️ ; Improve accessibility.
        💡 ; Add or update comments in source code.
        🍻 ; Write code drunkenly.
        💬 ; Add or update text and literals.
        🗃️ ; Perform database related changes.
        🔊 ; Add or update logs.
        🔇 ; Remove logs.
        👥 ; Add or update contributor(s).
        🚸 ; Improve user experience / usability.
        🏗️ ; Make architectural changes.
        📱 ; Work on responsive design.
        🤡 ; Mock things.
        🥚 ; Add or update an easter egg.
        🙈 ; Add or update a .gitignore file.
        📸 ; Add or update snapshots.
        ⚗️ ; Perform experiments.
        🔍️ ; Improve SEO.
        🏷️ ; Add or update types.
        🌱 ; Add or update seed files.
        🚩 ; Add, update, or remove feature flags.
        🥅 ; Catch errors.
        💫 ; Add or update animations and transitions.
        🗑️ ; Deprecate code that needs to be cleaned up.
        🛂 ; Work on code related to authorization, roles and permissions.
        🩹 ; Simple fix for a non-critical issue.
        🧐 ; Data exploration/inspection.
        ⚰️ ; Remove dead code.
        🧪 ; Add a failing test.
        👔 ; Add or update business logic.
        🩺 ; Add or update healthcheck.
        🧱 ; Infrastructure related changes.
        🧑‍💻 ; Improve developer experience.
        💸 ; Add sponsorships or money related infrastructure.
        🧵 ; Add or update code related to multithreading or concurrency.
        🦺 ; Add or update code related to validation.
    The title shall be formated as "{emoji} {title}"
    ''',
        'simple':'''
    For the title of your message use the GitMoji Convetion, here is some help emoji ; description:":
        ⚡️ ; Improve performance.
        🐛 ; Fix a bug.
        🚑️ ; Critical hotfix.
        ✨ ; Introduce new features.
        📝 ; Add or update documentation.
        ✅ ; Add, update, or pass tests.
        🔒️ ; Fix security or privacy issues.
        🔖 ; Release / Version tags.
        🚨 ; Fix compiler / linter warnings.
        ⬇️ ; Downgrade dependencies.
        ⬆️ ; Upgrade dependencies.
        ♻️ ; Refactor code.
        ➕ ; Add a dependency.
        ➖ ; Remove a dependency.
        🔧 ; Add or update configuration files.
        🌐 ; Internationalization and localization.
        ✏️ ; Fix typos.
        🚚 ; Move or rename resources (e.g.: files, paths, routes).
        💥 ; Introduce breaking changes.
        🍱 ; Add or update assets.
        ♿️ ; Improve accessibility.
        💡 ; Add or update comments in source code.
        🗃️ ; Perform database related changes.
        🚸 ; Improve user experience / usability.
        🏗️ ; Make architectural changes.
        🤡 ; Mock things.
        🥚 ; Add or update an easter egg.
        🙈 ; Add or update a .gitignore file.
        📸 ; Add or update snapshots.
        ⚗️ ; Perform experiments.
        🏷️ ; Add or update types.
        🥅 ; Catch errors.
        🧐 ; Data exploration/inspection.
        ⚰️ ; Remove dead code.
        🧪 ; Add a failing test.
        👔 ; Add or update business logic.
        🩺 ; Add or update healthcheck.
        💸 ; Add sponsorships or money related infrastructure.
    The title shall be formated as "{emoji} {title}"
    ''',
    'emoji_agent':'''
    Your mission is to recive a commit message and return an emoji based on the folowing guide.
    Do not explain yourself, return only the single emoji.
    '''
    }
        
}
