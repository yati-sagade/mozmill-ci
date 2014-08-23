import os
from os.path import dirname, abspath, join
from selenium import webdriver


# This environment variable should contain the path to the Jenkins directory.
ENV_JENKINS_HOME = 'JENKINS_HOME'


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
    assert len(jobs) == _jenkins_job_count(),\
            'Incorrect number of jobs for Jenkins.'

    for i, job in enumerate(jobs):
        driver.get(job['href'] + 'configure')
        print '[%d/%d] %s' % (i + 1, len(jobs), job['name'])
        driver.find_element_by_css_selector(
            '#bottom-sticker .submit-button button').click()
        driver.find_element_by_css_selector('#main-panel h1')

    driver.quit()


def _jenkins_job_count():
    """Return the number of jobs listed in the directory contained in the
    environment variable JENKINS_HOME. Each directory in $JENKINS_HOME
    corresponds to a job.

    """
    try:
        jenkins_home = os.environ[ENV_JENKINS_HOME] 
    except KeyError:
        raise Exception('The environment variable {} must be set to the '
                        'location of the Jenkins root directory.'
                        .format(ENV_JENKINS_HOME))
    jenkins_jobs_dir = os.path.join(jenkins_home, 'jobs')
    return len(os.walk(jenkins_jobs_dir).next()[1])


if __name__ == "__main__":
    main()
