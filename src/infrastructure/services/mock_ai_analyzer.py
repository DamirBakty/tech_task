class MockAIAnalyzer:
    """Mock AI analyzer that generates analysis based on file metadata."""

    async def analyze(self, file_content: bytes, file_name: str) -> str:
        file_size = len(file_content)
        version = 1
        
        # Generate analysis based on file characteristics
        size_mb = file_size / (1024 * 1024)
        
        if size_mb < 0.1:
            size_comment = "Файл очень маленький"
        elif size_mb < 1:
            size_comment = "Файл относительно небольшой"
        elif size_mb < 10:
            size_comment = "Файл среднего размера"
        else:
            size_comment = "Файл достаточно большой"
        
        if version == 1:
            version_comment = "Это первая версия документа."
        elif version == 2:
            version_comment = "Это вторая версия, были внесены изменения."
        else:
            version_comment = f"Это версия {version}, документ активно обновляется."
        
        # Determine file type
        file_extension = file_name.split(".")[-1].lower() if "." in file_name else "unknown"
        
        type_comments = {
            "pdf": "PDF документ, вероятно содержит текст и возможно изображения.",
            "docx": "Word документ, текстовый файл с форматированием.",
            "png": "PNG изображение, возможно скриншот или диаграмма.",
            "jpg": "JPEG изображение, возможно фотография.",
            "jpeg": "JPEG изображение, возможно фотография.",
            "txt": "Текстовый файл без форматирования.",
        }
        
        type_comment = type_comments.get(
            file_extension,
            f"Файл формата {file_extension.upper()}."
        )
        
        analysis = f"{size_comment} ({size_mb:.2f} MB). {version_comment} {type_comment}"
        
        if version > 1:
            analysis += " Новое изменение может содержать важные обновления."
        
        return analysis
