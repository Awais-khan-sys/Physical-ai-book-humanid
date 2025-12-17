/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: 'Introduction',
    },
    {
      type: 'doc',
      id: 'chapter1-foundations',
      label: 'Chapter 1: Foundations',
    },
    {
      type: 'doc',
      id: 'chapter2-perception',
      label: 'Chapter 2: Perception Systems',
    },
    {
      type: 'doc',
      id: 'chapter3-control',
      label: 'Chapter 3: Control & Actuation',
    },
    {
      type: 'doc',
      id: 'chapter4-ai-learning',
      label: 'Chapter 4: AI & Learning',
    },
    {
      type: 'doc',
      id: 'chapter5-applications',
      label: 'Chapter 5: Applications & Future',
    },
  ],
};

module.exports = sidebars;
