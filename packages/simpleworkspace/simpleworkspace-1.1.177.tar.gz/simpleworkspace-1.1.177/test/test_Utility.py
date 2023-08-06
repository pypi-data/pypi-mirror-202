import os
import simpleworkspace as sw
import time
from simpleworkspace.utility.stopwatch import StopWatch
from simpleworkspace.utility import bytes
from simpleworkspace.utility import regex
import gzip
from basetestcase import BaseTestCase



class Utility_ByteTests(BaseTestCase):
    def test_IsPotentiallyBinary(self):
        # Test case 1: Empty input
        assert not bytes.IsPotentiallyBinary(b"")

        # Test case 2: Input contains only printable ASCII characters
        assert not bytes.IsPotentiallyBinary(b"Hello World!")

        # Test case 3: Input contains control characters
        assert bytes.IsPotentiallyBinary(b"\x01\x02\x03\x0A\x09\x0D\x1B")

        # Test case 4: Input contains non-printable ASCII characters
        assert bytes.IsPotentiallyBinary(b"Hello \x01\x02\xA0 World!")

        # Test case 5: Input contains binary data (PNG file header)
        assert bytes.IsPotentiallyBinary(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")

        # Test case 6: Input contains binary data (GIF file header)
        assert bytes.IsPotentiallyBinary(b"GIF89a\x01\x00\x01\x00\x80\x01\x00\x00\x00")

        # Test case 7: Input is longer than sniffLen
        assert not bytes.IsPotentiallyBinary(b"Hello World!" * 100, sniffLen=10)

        # Test case 8: Input contains binary data after max sniffLen
        assert not bytes.IsPotentiallyBinary(b"123456789" + b"\x01\x02\x03" + b"321", sniffLen=9)
        assert bytes.IsPotentiallyBinary(b"123456789" + b"\x01\x02\x03" + b"321", sniffLen=10)


class Utility_RegexTests(BaseTestCase):
    sampleText = "Hello person1 with short hair\n" "Hello person2 with shoes\n" "Hello person3 with jacket\n" "this is a new walkthrough of version 1.2.8.12 of this app\n" "older available versions are following: v1.2.8.11, v1.2.8.10, v1.2.5.1, v1.1.2.9,\n" "good luck\n"

    def test_Regex_replace_flag_MultiLine(self):
        res = regex.Replace(r"/^Hello person(.) /", r"Hello bobby0 ", self.sampleText)
        resReplaced = regex.Match(r"/bobby. /i", res)
        expected = [
            ["bobby0 "],
            ["bobby0 "],
            ["bobby0 "],
        ]
        self.assertEqual(resReplaced, expected)

        res = regex.Replace(r"/person(.) /", r"bobby\1 ", self.sampleText)
        resReplaced = regex.Match(r"/bobby. /i", res)
        expected = [
            ["bobby1 "],
            ["bobby2 "],
            ["bobby3 "],
        ]
        self.assertEqual(resReplaced, expected)

        result = regex.Replace(r"/hej (.*?) /i", r"bye \1 or \g<1> ", "hej v1.0 hej v2.2 hejsan v3.3")  # result = "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3"
        self.assertEqual(result,  "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3")

    def test_Regex_replace_flag_DotAll(self):
        res = regex.Replace(r"/^Hello person(.) /s", r"bobby0 ", self.sampleText)
        resReplaced = regex.Match(r"/bobby. /i", res)
        expected = [["bobby0 "]]
        self.assertEqual(resReplaced, expected)

    def test_Regex_Match_flag_MultiLine(self):
        res = regex.Match(r"/^Hello (person.*?) /", self.sampleText)
        expected = [
            ["Hello person1 ", "person1"],
            ["Hello person2 ", "person2"],
            ["Hello person3 ", "person3"],
        ]
        self.assertEqual(res, expected)

    def test_Regex_Match_flag_DotAll(self):
        res = regex.Match(r"/^Hello (person.*?) /s", self.sampleText)
        expected = [
            ["Hello person1 ", "person1"],
        ]
        self.assertEqual(res,  expected)

        res = regex.Match(r"/^Hello.*(with) (jacket)/s", self.sampleText)
        expected = [["Hello person1 with short hair\nHello person2 with shoes\nHello person3 with jacket", "with", "jacket"],]
        self.assertEqual(res,  expected)

    def test_Regex_flag_CaseSensitivity(self):
        res = regex.Match(r"/hello person\d/", self.sampleText)
        self.assertIsNone(res)
        res = regex.Match(r"/Hello person\d/", self.sampleText)
        expected = [
            ["Hello person1"],
            ["Hello person2"],
            ["Hello person3"],
        ]
        self.assertEqual(res,  expected)

    ###AI generated auto tests###
    def test_AutoGen_Regex_no_match(self):
        pattern = r'/hello\s+world/'
        string = 'goodbye world'
        self.assertIsNone(regex.Match(pattern, string))

    def test_AutoGen_Regex_single_match(self):
        pattern = r'/hello\s+(\w+)/'
        string = 'hello world'
        expected_result = [['hello world', 'world']]
        self.assertEqual(regex.Match(pattern, string), expected_result)


    def test_AutoGen_Regex_multiple_matches(self):
        pattern = r'/hello\s+(\w+)/'
        string = 'hello world, hello john'
        expected_result = [['hello world', 'world'], ['hello john', 'john']]
        self.assertEqual(regex.Match(pattern, string), expected_result)

    def test_AutoGen_Regex_case_insensitive_match(self):
        pattern = r'/hello\s+(\w+)/i'
        string = 'HeLLo WoRlD'
        expected_result = [['HeLLo WoRlD', 'WoRlD']]
        self.assertEqual(regex.Match(pattern, string), expected_result)

    def test_AutoGen_Regex_dotall_match(self):
        pattern = r'/hello.+world/is'
        string = 'hello\nmultiline\nworld'
        expected_result = [['hello\nmultiline\nworld']]
        self.assertEqual(regex.Match(pattern, string), expected_result)

    def test_AutoGen_Regex_capture_group(self):
        pattern = r'/hello\s+(?P<name>\w+)/'
        string = 'hello world'
        expected_result = [['hello world', 'world']]
        self.assertEqual(regex.Match(pattern, string), expected_result)

    def test_AutoGen_Regex_multiple_capture_groups(self):
        pattern = r'/hello\s+(?P<first>\w+)\s+(?P<last>\w+)/'
        string = 'hello john doe'
        expected_result = [['hello john doe', 'john', 'doe']]
        self.assertEqual(regex.Match(pattern, string), expected_result)

    def test_AutoGen_Regex_replace_no_matches(self):
        pattern = r"/hej (.*?) /i"
        replacement = "bye \\1 or \g<1> "
        message = "hello world"
        expected = "hello world"
        actual = regex.Replace(pattern, replacement, message)
        self.assertEqual(expected, actual)

    def test_AutoGen_Regex_replace_with_matches(self):
        pattern = r"/hej (.*?) /i"
        replacement = "bye \\1 or \g<1> "
        message = "hej v1.0 hej v2.2 hejsan v3.3"
        expected = "bye v1.0 or v1.0 bye v2.2 or v2.2 hejsan v3.3"
        actual = regex.Replace(pattern, replacement, message)
        self.assertEqual(expected, actual)

    def test_AutoGen_Regex_replace_with_backreference(self):
        pattern = r"/(\d+)/i"
        replacement = r"\1-\g<1>"
        message = "abc 123 def 456 ghi 789"
        expected = "abc 123-123 def 456-456 ghi 789-789"
        actual = regex.Replace(pattern, replacement, message)
        self.assertEqual(expected, actual)

    def test_Regex_replace_multiple_occurrences(self):
        pattern = r"/\d+/"
        replacement = "number"
        message = "I have 5 apples and 10 oranges. My friend has 3 bananas and 5 grapes."
        expected = "I have number apples and number oranges. My friend has number bananas and number grapes."
        actual = regex.Replace(pattern, replacement, message)
        self.assertEqual(expected, actual)

class Utility_StopWatchTest(BaseTestCase):
    allowedDiffMS = 1

    def AccurateSleepMS(self, ms):
        start = time.perf_counter()
        time.sleep(ms / 1000)
        elapsed = time.perf_counter() - start
        return elapsed * 1000

    def InDistance(self, val1, val2, maxDistance):
        distance = abs(val1 - val2)
        if distance > maxDistance:
            return False
        return True

    def test_HappyFlow(self):
        #we do delta 1ms resolution, this means that just retrieving the time from stopwatch may take up to 1ms in theory
        stopWatch = StopWatch()

        res = stopWatch.GetElapsedMilliseconds()
        self.assertEqual(res, 0)

        stopWatch.Start()
        actualSleepTime = self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta=self.allowedDiffMS)

        # should do nothing since already running
        stopWatch.Start()
        stopWatch.Start()

        actualSleepTime += self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= self.allowedDiffMS)

        stopWatch.Stop()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= self.allowedDiffMS)

        self.AccurateSleepMS(1)  # skip this, since we just want to check if not counted after Stopped timer
        self.assertAlmostEqual(res,actualSleepTime, delta= self.allowedDiffMS)

        stopWatch.Start()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= self.allowedDiffMS)

        actualSleepTime += self.AccurateSleepMS(1)
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= self.allowedDiffMS)

        stopWatch.Start()
        stopWatch.Stop()
        stopWatch.Start()
        stopWatch.Stop()
        stopWatch.Start()
        stopWatch.Stop()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertAlmostEqual(res,actualSleepTime, delta= self.allowedDiffMS)

        stopWatch.Reset()
        res = stopWatch.GetElapsedMilliseconds()
        self.assertEqual(res, 0, f"should be 0 ms since we resetted time")
    
    def test_ContextManager(self):
        with StopWatch() as sw1:
            res = sw1.GetElapsedMilliseconds()
            self.assertAlmostEqual(res,0, delta=self.allowedDiffMS)
            
            actualSleepTime = self.AccurateSleepMS(1)
            res = sw1.GetElapsedMilliseconds()
            self.assertAlmostEqual(res,actualSleepTime, delta=self.allowedDiffMS)

        #out of contextmanager, timer should be stopped
        res1 = sw1.GetElapsedMilliseconds()
        actualSleepTime = self.AccurateSleepMS(1)
        res2 = sw1.GetElapsedMilliseconds()
        self.assertEqual(res1,res2)
        return

class Utility_RotatingLogFileReader(BaseTestCase):
    def CreateLog(self, logname = "tmp.log"):
        logPath = f"{self.testPath}/{logname}"
        sw.io.file.Create(logPath, "1\n2\n3\n")
        return logPath
    
    def CreateLog_Delayed_NoCompressions(self):
        logpath = self.CreateLog()
        os.rename(logpath, logpath + ".1")
        sw.io.file.Create(logpath, "4\n5\n6\n")
        return logpath
    
    def CreateLog_Delayed_WithCompressions(self):
        logpath = self.CreateLog_Delayed_NoCompressions()

        with open(f"{logpath}.1", 'rb') as f_in, gzip.open(f"{logpath}.2.gz", 'wb') as f_out:
            f_out.writelines(f_in)
        os.replace(f"{logpath}", f"{logpath}.1")
        sw.io.file.Create(logpath, "7\n8\n9\n")
        return logpath
    
    def CreateLog_WithCompression(self):
        logpath = self.CreateLog()
        
        with open(f"{logpath}", 'rb') as f_in, gzip.open(f"{logpath}.1.gz", 'wb') as f_out:
            f_out.writelines(f_in)
        sw.io.file.Create(logpath, "4\n5\n6\n")
        return logpath
    

    def test_SingleLogFile(self):
        logpath = self.CreateLog()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n"
        )

    def test_DelayedLog_withNoCompressedFiles(self):
        logpath = self.CreateLog_Delayed_NoCompressions()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n"
        )
    
    def test_DelayedLog_withCompressedFiles(self):
        logpath = self.CreateLog_Delayed_WithCompressions()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n7\n8\n9\n"
        )

    def test_OnlyCompressedFiles(self):
        logpath = self.CreateLog_WithCompression()
        self.assertEqual(
            sw.utility.log.RotatingLogReader(logpath).ToString(),
            "1\n2\n3\n4\n5\n6\n"
        )