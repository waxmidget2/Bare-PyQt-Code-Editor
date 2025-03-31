from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document, language='Python'):
        super().__init__(document)
        self.language = language
        self.highlighting_rules = []
        
        # Language keywords dictionary (truncated for brevity, you can expand this)
        language_keywords = {
            'Python': [
                'and', 'assert', 'break', 'class', 'continue', 'def',
                'del', 'elif', 'else', 'except', 'finally', 'for',
                'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
                'nonlocal', 'not', 'or', 'pass', 'raise', 'return',
                'try', 'while', 'with', 'yield', 'None', 'True', 'False',
                'print'
            ],
            'C++': [
                'auto', 'break', 'case', 'catch', 'class', 'const', 'continue',
                'default', 'delete', 'do', 'else', 'enum', 'explicit', 'export',
                'extern', 'for', 'friend', 'if', 'inline', 'mutable', 'namespace',
                'new', 'operator', 'private', 'protected', 'public', 'return',
                'sizeof', 'static', 'struct', 'switch', 'template', 'this',
                'throw', 'try', 'typedef', 'typeid', 'typename', 'union',
                'using', 'virtual', 'while', 'int', 'float', 'double', 'char',
                'bool', 'void', 'return', 'nullptr'
            ],
            'Java': [
                'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch',
                'char', 'class', 'const', 'continue', 'default', 'do', 'double',
                'else', 'enum', 'extends', 'final', 'finally', 'float', 'for',
                'if', 'implements', 'import', 'instanceof', 'int', 'interface',
                'long', 'native', 'new', 'null', 'package', 'private', 'protected',
                'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch',
                'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
                'void', 'volatile', 'while'
            ],
            'JavaScript': [
                'break', 'case', 'catch', 'class', 'const', 'continue', 'debugger',
                'default', 'delete', 'do', 'else', 'export', 'extends', 'finally',
                'for', 'function', 'if', 'import', 'in', 'instanceof', 'new', 'return',
                'super', 'switch', 'this', 'throw', 'try', 'typeof', 'var', 'void',
                'while', 'with', 'yield', 'null', 'true', 'false', 'async', 'await'
            ],
            'Rust': [
                'as', 'break', 'const', 'continue', 'crate', 'dyn', 'else', 'enum',
                'extern', 'false', 'fn', 'for', 'if', 'impl', 'in', 'let', 'loop',
                'match', 'mod', 'move', 'mut', 'pub', 'ref', 'return', 'self', 'static',
                'struct', 'super', 'trait', 'true', 'type', 'unsafe', 'use', 'where',
                'while'
            ],
            'Swift': [
                'break', 'case', 'catch', 'class', 'continue', 'default', 'defer',
                'do', 'else', 'enum', 'extension', 'fallthrough', 'for', 'guard',
                'if', 'in', 'is', 'let', 'mutating', 'protocol', 'return', 'static',
                'struct', 'switch', 'throw', 'throws', 'try', 'var', 'where', 'while',
                'nil', 'true', 'false', 'init', 'deinit', 'subscript'
            ],
            'Go': [
                'break', 'case', 'chan', 'const', 'continue', 'default', 'defer',
                'else', 'fallthrough', 'for', 'func', 'go', 'goto', 'if', 'import',
                'interface', 'map', 'package', 'range', 'return', 'select', 'struct',
                'switch', 'type', 'var', 'nil', 'true', 'false'
            ],
            'Ruby': [
                'alias', 'and', 'begin', 'break', 'case', 'class', 'def', 'defined?',
                'do', 'else', 'elsif', 'end', 'ensure', 'false', 'for', 'if', 'in',
                'module', 'next', 'nil', 'not', 'or', 'redo', 'rescue', 'retry',
                'return', 'self', 'super', 'then', 'true', 'undef', 'unless', 'until',
                'when', 'while', 'yield'
            ],
            'PHP': [
                'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch',
                'class', 'clone', 'const', 'continue', 'declare', 'default', 'die',
                'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor',
                'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit', 'extends',
                'final', 'finally', 'for', 'foreach', 'function', 'global', 'goto',
                'if', 'implements', 'include', 'include_once', 'instanceof', 'insteadof',
                'interface', 'isset', 'list', 'namespace', 'new', 'or', 'print', 'private',
                'protected', 'public', 'require', 'require_once', 'return', 'static',
                'switch', 'throw', 'trait', 'try', 'unset', 'use', 'var', 'while', 'xor'
            ],
            'Kotlin': [
                'as', 'break', 'class', 'continue', 'do', 'else', 'false', 'for', 'fun',
                'if', 'in', 'interface', 'is', 'null', 'object', 'package', 'return',
                'super', 'this', 'throw', 'true', 'try', 'typealias', 'val', 'var',
                'when', 'while'
            ],
            'TypeScript': [
                'abstract', 'any', 'as', 'break', 'case', 'catch', 'class', 'const',
                'continue', 'debugger', 'default', 'delete', 'do', 'else', 'enum',
                'export', 'extends', 'false', 'finally', 'for', 'function', 'if',
                'implements', 'import', 'in', 'instanceof', 'interface', 'let', 'new',
                'null', 'private', 'protected', 'public', 'return', 'static', 'super',
                'switch', 'this', 'throw', 'true', 'try', 'type', 'typeof', 'var',
                'void', 'while', 'with', 'yield'
            ]
        }
        
        # Keyword formatting
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('#f1cc00'))
        
        # Get keywords for the current language
        keywords = language_keywords.get(language, [])
        
        for word in keywords:
            pattern = r'\b' + word + r'\b'
            self.highlighting_rules.append((pattern, keyword_format))
        
        object_format = QTextCharFormat()
        object_format.setForeground(QColor('#3aafdc'))
        returnTypeList = ['self', 'void', 'return', ]
        self.highlighting_rules.append((r'\b\w+(?=\s*\()', object_format))
        self.returnRuleAndSelf = QTextCharFormat()
        self.returnRuleAndSelf.setForeground(QColor("#FE4EDA"))
        for returnType in returnTypeList:
            self.highlighting_rules.append((returnType, self.returnRuleAndSelf))
        bracket_format = QTextCharFormat()
        bracket_error = QTextCharFormat()
        bracket_error = QTextCharFormat()
        bracket_error.setForeground(QColor('#ff0000'))  # Red for errors
# Optionally add background highlighting for errors
        bracket_error.setBackground(QColor('#332222'))
        bracket_format.setForeground(QColor('#ffffff'))
        self.highlighting_rules.append((r'\(', bracket_format))
# For highlighting matched pairs of brackets with content between them
        self.highlighting_rules.append((r'\([^\(\)]*\)', bracket_format))
        
        # String formatting 
        string_format = QTextCharFormat()
        string_format.setForeground(QColor('#ce9178'))
        self.highlighting_rules.append((r'"[^"\\]*(\\.[^"\\]*)*"', string_format))
        self.highlighting_rules.append((r"'[^'\\]*(\\.[^'\\]*)*'", string_format))

        # Comment formatting
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor('#6a9955'))
        self.highlighting_rules.append((r'#[^\n]*', comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
