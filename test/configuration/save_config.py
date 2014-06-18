import os
from os.path import dirname, abspath, join
from selenium import webdriver


def main():
    base_url = 'http://localhost:8080/'

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(10)

    print 'Saving main configuration...'
    driver.get(base_url + 'configure')
    driver.find_element_by_css_selector(
        '#bottom-sticker .submit-button button').click()

    print 'Saving node configurations...'
    driver.get(base_url + 'computer/')
    node_links = driver.find_elements_by_css_selector(
        "tr[id*='node_'] > td:nth-child(2) > a")
    nodes = [{'name': link.text, 'href': link.get_attribute('href')} for
             link in node_links]

    for i, node in enumerate(nodes):
        driver.get(node['href'] + 'configure')
        print '[%d/%d] %s' % (i + 1, len(nodes), node['name'])
        driver.find_element_by_css_selector('.submit-button button').click()
        driver.find_element_by_css_selector('#main-panel h1')

    print 'Saving job configurations...'
    driver.get(base_url)
    job_links = driver.find_elements_by_css_selector(
        "tr[id*='job_'] > td:nth-child(3) > a")
    jobs = [{'name': link.text, 'href': link.get_attribute('href')} for
            link in job_links]
    assert len(jobs) == _jenkins_job_count(), 'No jobs configured in Jenkins!'

    for i, job in enumerate(jobs):
        driver.get(job['href'] + 'configure')
        print '[%d/%d] %s' % (i + 1, len(jobs), job['name'])
        driver.find_element_by_css_selector(
            '#bottom-sticker .submit-button button').click()
        driver.find_element_by_css_selector('#main-panel h1')

    driver.quit()


def _jenkins_job_count():
    """Return the number of jobs listed in the directory ../../jenkins-master.
    Each job is a directory.

    """
    jenkins_master_dir =  join(dirname(dirname(dirname(abspath(__file__)))),
                               join('jenkins-master', 'jobs'))
    return len(os.walk(jenkins_master_dir).next()[1])


if __name__ == "__main__":
    main()
