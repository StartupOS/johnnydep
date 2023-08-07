from curses.ascii import isdigit
import json
import os
from pathlib import Path
from typing import List, TextIO
import xml

class Entry(dict):
    def __init__(self,
        name:str,
        source:str,
        specifier:str,
        license,
        requires,
        required_by,
        summary:str
    )->None:
        if not name:
            raise Exception("Entries must have a package name")
        if not source:
            raise Exception("Entries must have a package source")
        
        self.name=name
        self.source=source
        self.specifier=specifier
        self.license=license
        self.requires=requires
        self.required_by=required_by
        self.summary=summary

class Walker():
    def __init__(self, 
        manifest_type:str, #"json", 
        manifest_files:List[str] #["package.json"]
        ) -> None:
        self.files=[]
        self.manifest_files=manifest_files
        self.manifest_type=manifest_type
        self.entries = []

    def walk(self, path:str="./", parse:bool=True, expand:bool=False):
        for pattern in self.manifest_files:
            glob =  "**/" + pattern
            for p in Path(path).rglob(glob):
                self.files.append(p)
                if parse:
                    self.parse(file=p, expand=expand)
        
    def parse(self, file, expand=False):
        raise Exception("No parser for this Walker")

    def expand(self, file):
        raise Exception("No expansion for this Walker")
    
class MavenWalker(Walker):
    # pkg:maven/springframework/spring@1.2.6
    # mvn license:aggregate-add-third-party
    # mvn dependency:analyze
    # mvn dependency-check:check
    # mvn org.sonatype.ossindex.maven:ossindex-maven-plugin:audit -f pom.xml
    # <project>
    # ...
    # <properties>
    # <mavenVersion>3.0</mavenVersion>
    # </properties>

    # <dependencies>
    # <dependency>
    #     <groupId>org.apache.maven</groupId>
    #     <artifactId>maven-artifact</artifactId>
    #     <version>${mavenVersion}</version>
    # </dependency>
    # <dependency>
    #     <groupId>org.apache.maven</groupId>
    #     <artifactId>maven-core</artifactId>
    #     <version>${mavenVersion}</version>
    # </dependency>
    # </dependencies>
    # ...
    # </project>

    def parse(self, file:TextIO, expand=False):
        parser = xml.parsers.expat.ParserCreate()
        parser.ParseFile(file)
        parser.
        raise Exception("No parser for this Walker")

    def expand(self, file):
        raise Exception("No expansion for this Walker")

mavenWalker = Walker(manifest_type="xml", manifest_files=["pom.xml"])
